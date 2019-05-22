from gym_voilier.envs.roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py 
    
def f(x,u, params):
    x,u=x.flatten(),u.flatten()
    θ=x[2]; v=x[3]; w=x[4]; δr=u[0]; δsmax=u[1]
    w_ap = array([[params['awind']*cos(params['ψ']-θ) - v],[params['awind']*sin(params['ψ']-θ)]])
    ψ_ap = angle(w_ap)
    a_ap=norm(w_ap)
    sigma = cos(ψ_ap) + cos(δsmax)
    if sigma < 0 :
        δs = pi + ψ_ap
    else :
        δs = -sign(sin(ψ_ap))*δsmax
    fr = params['p4']*v*sin(δr)
    fs = params['p3']*a_ap* sin(δs - ψ_ap)
    dx=v*cos(θ) + params['p0']*params['awind']*cos(params['ψ'])
    dy=v*sin(θ) + params['p0']*params['awind']*sin(params['ψ'])
    dv=(fs*sin(δs)-fr*sin(δr)-params['p1']*v**2)/params['p8']
    dw=(fs*(params['p5']-params['p6']*cos(δs)) - params['p7']*fr*cos(δr) - params['p2']*w*v)/params['p9']
    xdot=array([ [dx],[dy],[w],[dv],[dw]])
    return xdot,δs        

def step(x, u, dt, params):
    
    xdot,δs=f(x, u, params)
    x_new = x + dt*xdot
    return x_new, δs

if __name__ == '__main__':

    params = {
        'awind':    2,      # wind force
        'ψ':        -1.57,  # wind angle
        'p0':        0.1,
        'p1':        1,
        'p2':        6000,
        'p3':        1000,
        'p4':        2000,
        'p5':        1,
        'p6':        1,
        'p7':        2,
        'p8':        300,
        'p9':        10000
    }
    
    # initial state
    x = array([[10,-40,-3,1,0]]).T   #x=(x,y,θ,v,w)

    a = array([[-50],[-100]])   
    b = array([[50],[100]])
    ax=init_figure(-100,100,-60,60)

    for t in arange(0,20,0.1):
        clear(ax)
        plot([a[0,0],b[0,0]],[a[1,0],b[1,0]],'red')

        #u=array([[0],[1]])
        u = array([[pi/2], [pi/4]])

        x, δs = step(x, u, 0.1, params)
        
        
        draw_sailboat(x,δs,u[0,0],params['ψ'],params['awind'])


        