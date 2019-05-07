import numpy as np
import matplotlib.pyplot as plt
import scipy as sci


data = np.genfromtxt('polarplot.csv', delimiter = ';')
#print(data)

real_theta = np.zeros((22,7))
theta_grad = data[2:,0]
theta = data[2:, 0]*np.pi/180  # radians
for i in range(len(theta)):
    real_theta[i,:]=theta[i]
speed_values = data[2:, 1:] 


#print(speed_values)
#print(theta_grad)
#print(real_theta[0])

ax = plt.subplot(111, projection='polar')
ax.plot(real_theta,speed_values)
ax.set_rmax(10)
r = np.arange(2,10,2)
ax.set_rticks(r)
ax.set_rlabel_position(-22.5)
ax.grid(True)

plt.show()

# Use machine learning to Interpolar angle values in middle. Polynomial Interpolation


