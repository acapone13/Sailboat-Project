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

    def interpolate(self,speed,theta):
        downAngle = max([s for s in self.theta_grad if theta >= s])
        upAngle = min([s for s in self.theta_grad if theta <= s])
        downSpeed = max([s for s in self.wind_speed if speed >= s])
        upSpeed = min([s for s in self.wind_speed if speed <= s])
        
        for i in range(len(self.theta_grad)):
            if self.theta_grad[i] == downAngle:
                indexA1 = i
            if self.theta_grad[i] == upAngle:
                indexA2 = i

        for i in range(len(self.wind_speed)):
            if self.wind_speed[i] == downSpeed:
                indexS1 = i 
            if self.wind_speed[i] == upSpeed:
                indexS2 = i

        self.boat_speed = (self.speed_values[indexA1,indexS1]/(abs(self.speed_values[indexA1,indexS1] - speed)) + self.speed_values[indexA2,indexS2]/(abs(self.speed_values[indexA2,indexS2] - speed)))/((1/abs(self.speed_values[indexA1,indexS1] - speed)) + (1/abs(self.speed_values[indexA2,indexS2] - speed)))
        self.boat_angle = (self.theta_grad[indexA1]/(abs(self.theta_grad[indexA1] - theta)) + self.theta_grad[indexA2]/(abs(self.theta_grad[indexA2] - theta)))/((1/abs(self.theta_grad[indexA1] - theta)) + (1/abs(self.theta_grad[indexA2] - theta)))


        # Modificate boat_angle

    def getBoatSpeed(self):
        return self.boat_speed

    def getBoatAngle(self):
        return self.boat_angle

    #def getMaxTWA(self, theta:
        #do NOthing
        

if __name__ == '__main__':
    pp = polarPlot()
    pp.interpolate(7.5,40)
    print(pp.getBoatSpeed(), pp.getBoatAngle())

