import numpy as np
import matplotlib.pyplot as plt
import scipy as sci

class polarPlot:
    def __init__(self):
        self.data = np.genfromtxt('polarplot.csv', delimiter = ',')
        self.real_theta = np.zeros((22,7))
        self.wind_speed  = self.data[0,1:]
        self.theta_grad = self.data[1:,0]
        self.theta = self.data[1:, 0]*np.pi/180  # radians
        for i in range(len(self.theta)):
            self.real_theta[i,:] = self.theta[i]
        self.speed_values = self.data[1:, 1:]
        self.boat_speed = 0
        self.boat_angle = 0

    def interpolate(self,speed, angle):
        downSpeed = max([s for s in self.wind_speed if speed >= s])
        upSpeed = min([s for s in self.wind_speed if speed <= s])
        downAngle = max([s for s in self.theta_grad if angle >= s])
        upAngle = min([s for s in self.theta_grad if angle <= s])

        for i in range(len(self.wind_speed)):
            if self.wind_speed[i] == downSpeed:
                indexS1 = i 
            if self.wind_speed[i] == upSpeed:
                indexS2 = i
        for i in range(len(self.theta_grad)):
            if self.theta_grad[i] == downAngle:
                indexA1 = i
            if self.theta_grad[i] == upAngle:
                indexA2 = i

        self.boat_speed = (self.speed_values[indexA1,indexS1]/(abs(self.speed_values[indexA1,indexS1] - speed)) + self.speed_values[indexA2,indexS2]/(abs(self.speed_values[indexA2,indexS2] - speed)))/((1/abs(self.speed_values[indexA1,indexS1] - speed)) + (1/abs(self.speed_values[indexA2,indexS2] - speed)))

    def getBoatSpeed(self):
        return self.boat_speed

    def getBoatAngle(self):
        return self.boat_angle

    def getTWA(self, speed, minTheta, maxTheta):
        downAngle = max([s for s in self.theta_grad if abs(minTheta) >= s])
        upAngle = min([s for s in self.theta_grad if abs(maxTheta) < s])
        #theta = self.getMaxTWA(speed, downAngle, upAngle)
        theta = (upAngle + downAngle)/2
        
        for i in range(len(self.theta_grad)):
            if self.theta_grad[i] == downAngle:
                indexA1 = i
            if self.theta_grad[i] == upAngle:
                indexA2 = i
        
        if (abs(self.theta_grad[indexA1] - theta) != 0 or abs(self.theta_grad[indexA2] - theta) != 0):
            self.boat_angle = (self.theta_grad[indexA1]/(abs(self.theta_grad[indexA1] - theta)) + self.theta_grad[indexA2]/(abs(self.theta_grad[indexA2] - theta)))/((1/abs(self.theta_grad[indexA1] - theta)) + (1/abs(self.theta_grad[indexA2] - theta)))
        else:
            self.boat_angle = 0# self.getMaxTWA(speed, theta)

        self.interpolate(speed,self.boat_angle)        

if __name__ == '__main__':
    pp = polarPlot()
    pp.getTWA(10,-120,-60)
    print(pp.getBoatSpeed(), pp.getBoatAngle())

