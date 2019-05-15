import numpy as np
import matplotlib.pyplot as plt
import scipy as sci

class polarPlot:
    def __init__(self):
        self.data = np.genfromtxt('polarplot.csv', delimiter = ';')
        self.real_theta = np.zeros((22,7))
        self.wind_speed  = self.data[0,1:]
        self.theta_grad = self.data[2:,0]
        self.theta = self.data[2:, 0]*np.pi/180  # radians
        for i in range(len(self.theta)):
            self.real_theta[i,:] = self.theta[i]
        self.speed_values = self.data[2:, 1:]

    def interpolate(self,speed,theta):
        thetaRad = theta*np.pi/180
        upAngle = min([s for s in self.theta if thetaRad < s])
        downAngle = max([s for s in self.theta if thetaRad > s])
        downSpeed = max([s for s in self.wind_speed if speed > s])
        upSpeed = min([s for s in self.wind_speed if speed < s])
        
        for i in range(len(self.theta)):
            if self.theta[i] == downAngle:
                indexA1 = i
            elif self.theta[i] == upAngle:
                indexA2 = i

        for i in range(len(self.wind_speed)):
            if self.wind_speed[i] == downSpeed:
                indexS1 = i 
            elif self.wind_speed[i] == upSpeed:
                indexS2 = i

        interSpeed = (self.speed_values[indexA1,indexS1]/(abs(self.speed_values[indexA1,indexS1] - speed)) + self.speed_values[indexA2,indexS2]/(abs(self.speed_values[indexA2,indexS2] - speed)))/((1/abs(self.speed_values[indexA1,indexS1] - speed)) + (1/abs(self.speed_values[indexA2,indexS2] - speed))) 

        return interSpeed




