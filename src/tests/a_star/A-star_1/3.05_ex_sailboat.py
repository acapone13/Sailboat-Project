from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py

         
    
def f(x,u):
    x,u=x.flatten(),u.flatten()
    θ=x[2]; v=x[3]; w=x[4]; δr=u[0]; δsmax=u[1];
    w_ap = array([[awind*cos(ψ-θ) - v],[awind*sin(ψ-θ)]])
    ψ_ap = angle(w_ap)
    a_ap=norm(w_ap)
    sigma = cos(ψ_ap) + cos(δsmax)
    if sigma < 0 :
        δs = pi + ψ_ap
    else :
        δs = -sign(sin(ψ_ap))*δsmax
    fr = p4*v*sin(δr)
    fs = p3*a_ap* sin(δs - ψ_ap)
    dx=v*cos(θ) + p0*awind*cos(ψ)
    dy=v*sin(θ) + p0*awind*sin(ψ)
    dv=(fs*sin(δs)-fr*sin(δr)-p1*v**2)/p8
    dw=(fs*(p5-p6*cos(δs)) - p7*fr*cos(δr) - p2*w*v)/p9
    xdot=array([ [dx],[dy],[w],[dv],[dw]])
    return xdot,δs    

    
    
    
    
p0,p1,p2,p3,p4,p5,p6,p7,p8,p9 = 0.1,1,6000,1000,2000,1,1,2,300,10000
x = array([[0.0,-50,1,1,0]]).T   #x=(x,y,θ,v,w)

dt = 0.1
awind,ψ = 2,-1.57 # 2,-2  
a = array([[-50],[-100]])   
b = array([[50],[100]])
                  
# ax=init_figure(-100,100,-60,60)

for t in arange(0,10,0.1):
    # dt = 0.5
    # clear(ax)
    # plot([a[0,0],b[0,0]],[a[1,0],b[1,0]],'red')
    # plot([a[0,0],b[0,0]],[a[1,0],b[1,0]],'red')

    # u speed array has 2 angles between -pi and pi to control rudder and sail
    # u = array ([[angle_ruder],[angle_sail]])
    u=array([[0],[1]])
    xdot,δs=f(x,u)
    x = x + dt*xdot
    print(x)
    # draw_sailboat(x,δs,u[0,0],ψ,awind)


        