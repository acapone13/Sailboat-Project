from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py 
from enum import Enum

class Params(object):
    p0 = 0.1
    p1 = 1
    p2 = 6000
    p3 = 1000
    p4 = 2000
    p5 = 1
    p6 = 1
    p7 = 2
    p8 = 300
    p9 = 10000


def f(x,u, wind):
    # wind = [awind, ψ]
    awind, ψ = wind
    x,u=x.flatten(),u.flatten()
    θ=x[2]; v=x[3]; w=x[4]; δr=u[0]; δsmax=u[1]
    w_ap = array([[awind*cos(ψ-θ) - v],[awind*sin(ψ-θ)]])
    ψ_ap = angle(w_ap)
    a_ap=norm(w_ap)
    sigma = cos(ψ_ap) + cos(δsmax)
    if sigma < 0 :
        δs = pi + ψ_ap
    else :
        δs = -sign(sin(ψ_ap))*δsmax
    fr = Params.p4*v*sin(δr)
    fs = Params.p3*a_ap* sin(δs - ψ_ap)
    dx=v*cos(θ) + Params.p0*awind*cos(ψ)
    dy=v*sin(θ) + Params.p0*awind*sin(ψ)
    dv=(fs*sin(δs)-fr*sin(δr)-Params.p1*v**2)/Params.p8
    dw=(fs*(Params.p5-Params.p6*cos(δs)) - Params.p7*fr*cos(δr) - Params.p2*w*v)/Params.p9
    xdot=array([ [dx],[dy],[w],[dv],[dw]])
    return xdot,δs        

def step(x, u, dt, wind):
    """
     This function makes a step of simmulation.
     Parameters:
        x: Actual state of the boat
        u: Angles for the rudder and the sail 
    Return values:
        x_new:  New state of the boat
        δs:     Actual angle of the sail
    """
    
    xdot,δs=f(x, u, wind)
    x_new = x + dt*xdot
    return x_new, δs

if __name__ == '__main__':

    wind = array([2, -1.57])
    
    # initial state
    x = array([[10,-40,-3,1,0]]).T   #x=(x,y,θ,v,w)

    a = array([[-50],[-100]])   
    b = array([[50],[100]])
    ax=init_figure(-100,100,-60,60)

    for t in arange(0,20,0.1):
        clear(ax)

        u = array([[pi/2], [pi/4]])

        x, δs = step(x, u, 0.1, wind)
        
        draw_sailboat(x,δs,u[0,0],wind[1],wind[0])



        