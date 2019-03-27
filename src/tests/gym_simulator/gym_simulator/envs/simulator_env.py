import gym
from gym import error, spaces, utils
from gym.utils import seeding
from roblib import *

class SailboatSimulatorEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.p = ([[0.1,1,6000,1000,2000,1,1,2,300,10000]])
        self.x0 = array([[0,-50,1.57,1,0]]).T   #x=(x,y,θ,v,w)
        self.x = self.x0

        self.dt = 0.1
        self.awind, self.ψ = 2,-1.57 # -2,-2 
        self.u = array([[-0.5],[1]])
    
    def step(self, action):
        for t in arange(0,10,0.1):
            xdot, δs = f(self.x, self.u)
            self.x = self.x + self.dt*xdot

    def reset(self):
        self.x = self.x0 

    def render(self, mode='human', close = False):
        print(x)

    def f(self, x, u):
        self.x, self.u = x.flatten(), u.flatten()
        θ=self.x[2]
        v=self.x[3]
        w=self.x[4]
        δr=self.u[0]
        δsmax=self.u[1]
        w_ap = array([[self.awind*cos(self.ψ-θ) - v],[self.awind*sin(self.ψ-θ)]])
        ψ_ap = angle(w_ap)
        a_ap=norm(w_ap)
        sigma = cos(ψ_ap) + cos(δsmax)
        if sigma < 0 :
            δs = pi + ψ_ap
        else :
            δs = -sign(sin(ψ_ap))*δsmax
        fr = p[4]*v*sin(δr)
        fs = p[3]*a_ap* sin(δs - ψ_ap)
        dx=v*cos(θ) + p[0]*awind*cos(ψ)
        dy=v*sin(θ) + p[0]*awind*sin(ψ)
        dv=(fs*sin(δs)-fr*sin(δr)-p[1]*v**2)/p8
        dw=(fs*(p[5]-p[6]*cos(δs)) - p[7]*fr*cos(δr) - p[2]*w*v)/p[9]
        xdot=array([ [dx],[dy],[w],[dv],[dw]])
        return xdot, δs