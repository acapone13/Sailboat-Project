import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import math
from gym_voilier.envs.roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
import gym_voilier.envs.sim

class VoilierEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.params = {
            'awind':    2,      # wind force [0, 10]
            'ψ':        -1.57,  # wind angle [-pi, pi]
            'p0':        0.1,   # ???
            'p1':        1,     # ???
            'p2':        6000,  # ???
            'p3':        1000,  # ???
            'p4':        2000,  # ???
            'p5':        1,     # ???
            'p6':        1,     # ???
            'p7':        2,     # ???
            'p8':        300,   # ???
            'p9':        10000  # ???
        }

        self.t_max = 200
        self.dt = 0.2
        self.max_sight = 40
        self.max_wind = 2

        self.reset()

        self.action_space = spaces.Box(np.array([-1, -1]), np.array([1, 1]), dtype=np.float32)
        self.observation_space = spaces.Box(np.array([-1, -1, -1, -1]), np.array([1, 1, 1, 1]), dtype=np.float32)

        #-----------------------------------------------------
        # Plot-Parameters
        #-----------------------------------------------------
        a = array([[-50],[-100]])   
        b = array([[50],[100]])
        figure_params = {
            'width' :   200,
            'height':   120
        }
        self.ax=init_figure(-figure_params['width']/2,figure_params['width']/2,-figure_params['height']/2,figure_params['height']/2)


    def step(self, action):

        # update wind
        forceChange = 0.5
        angleChange = 0.1*pi
        self.params['awind'] += np.random.uniform(-forceChange*self.dt, forceChange*self.dt, 1)[0]
        if self.params['awind'] > self.max_wind:
            self.params['awind'] = self.max_wind
        if self.params['awind'] < 0:
            self.params['awind'] = 0
        self.params['ψ'] += np.random.uniform(-angleChange*self.dt, angleChange*self.dt, 1)[0]
        if self.params['ψ'] > pi:
            self.params['ψ'] = -pi
        if self.params['ψ'] < -pi:
            self.params['ψ'] = pi

        self.u = array([action*pi/2.0])

        self.x, self.δs = gym_voilier.envs.sim.step(self.x, self.u, self.dt, self.params)

        boatDir = self.limitAngle(self.x[2][0])

        status, reward = self.get_reward(self.x[0:2,0], self.target)

        self.to_target = array([[self.target[0]-self.x[0][0], self.target[1]-self.x[1][0]]], dtype=np.float32)
        self.to_target = self.rotateVec(self.clampTarget(self.to_target, self.max_sight) / self.max_sight, boatDir)
        # print(self.to_target)

        self.wind = array([[self.params['awind']/self.max_wind, self.limitAngle(self.params['ψ']-boatDir)/pi]], dtype=np.float32)
        state = np.concatenate((self.to_target, self.wind), axis = None)

        done = (status == 'win' or status == 'lose')

        ###### observations, reward, finished, info
        return state, reward, done, {}
        

    def reset(self):
        self.params['awind'] = np.random.uniform(1, 10, 1)[0]
        self.params['ψ'] = np.random.uniform(-pi, pi, 1)[0]
        rndOrientation = np.random.uniform(-pi, pi, 1)[0]
        self.x = array([[0.0, 0.0, rndOrientation, 1, 0]]).T   #x=(x,y,θ,v,w)
        self.u = array([0, 1])

        targetRange = 20.0 #+ i_episode*0.001
        self.target = np.random.uniform(-targetRange,targetRange,2)

        return self.step(np.array([0,0]))[0]
        
    def render(self, mode='human', close=False):
        boatDir = self.limitAngle(self.x[2][0])
        clear(self.ax)
        plot(self.target[0], self.target[1], '*b')
        draw_sailboat(self.x,self.δs,self.u[0,0],self.params['ψ'],self.params['awind'])
        # draw_arrow(self.x[0][0], self.x[1][0], angle(self.rotateVec(self.to_target, -boatDir)), norm(self.to_target)*self.max_sight, 'blue')
        # draw_arrow(self.x[0][0], self.x[1][0], self.limitAngle(self.wind[0][1]*pi+boatDir), self.wind[0][0]*self.max_wind*5, 'cyan')
        draw_arrow(self.x[0][0], self.x[1][0], self.limitAngle(angle(self.to_target)+boatDir), norm(self.to_target)*self.max_sight, 'blue')

    # --------------------------------------------------------------------------------- #

    def clampTarget(self, target, dist=10.0):
        if norm(target) > dist:
            return target*dist/norm(target)
        return target

    def limitAngle(self, a):
        if a > pi:
            a = -pi + math.fmod(a,pi)
        elif a < -pi:
            a = pi - math.fmod(-a, pi)
        return a

    def rotateVec(self, xy, radians):
        """Only rotate a point around the origin (0, 0)."""
        x = xy[0][0]
        y = xy[0][1]
        xx = x * math.cos(radians) + y * math.sin(radians)
        yy = -x * math.sin(radians) + y * math.cos(radians)

        return array([[xx, yy]])

    def get_reward(self, pos, target):
        #HARDCODED!!!!!!!
        x = [-100, 100] # Map boundaries
        y = [-60, 60]   # Map boundaries
        status = 'not over'
        reward = 0
        if norm(target-pos) < 5:
            status = 'win'
            reward = 100
        elif (pos[0] > x[1] or pos[0] < x[0] or pos[1] < y[0] or pos[1]>y[1]):
            #Out of bondaries
            status = 'lose'
            reward = -100
        else:
            status = 'not over'
            reward = -(norm(target-pos))*0.1
        return (status, reward)
  