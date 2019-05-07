from polarplot import * # Get speed List

wind_speed = data[0,1:] # Real wind speeds
MaxSpeed_Starboard_bow = np.zeros((1,7)) # First maximal boat speeds speeds
MaxSpeed_Starboard_beam = np.zeros((1,7)) # Second maximal boat speeds
MaxSpeed_Starboard_quarter = np.zeros((1,7)) # Third maximal boat speeds

# Starboard:  Right, Port: Left, Forward, Aft:Backwards
# Starboard Bow: 0-75, Starboard Beam: 75-125, Starboard Quarter: 125-180


for i in range(len(wind_speed)):
    for j in range(len(theta_grad)):
        if (theta_grad[j] < 60):
            MaxSpeed_Starboard_bow[:,i] = max(speed_values[:9,i])
        elif (theta_grad[j] > 60 and theta_grad[j] < 125):
            MaxSpeed_Starboard_beam[:,i] = max(speed_values[10:13,i])
        elif (theta_grad[j] > 125):
            MaxSpeed_Starboard_quarter[:,i] = max(speed_values[13:,i])

# print(wind_speed)
#print(MaxSpeed_Starboard_bow)
#print(MaxSpeed_Starboard_beam)
#print(MaxSpeed_Starboard_quarter)

MaxAngles = np.zeros((1,3))

for i in range(len(wind_speed)):
    for j in range(len(theta_grad)):
        if (speed_values[j,i] == MaxSpeed_Starboard_bow[:,i]):
            MaxAngles[:,0] = theta_grad[j]
        elif (speed_values[j,i] == MaxSpeed_Starboard_beam[:,i] and (theta_grad[j] > 60 and theta_grad[j] < 125)):
            MaxAngles[:,1] = theta_grad[j]
        elif (speed_values[j,i] == MaxSpeed_Starboard_quarter[:,i]):
            MaxAngles[:,2] = theta_grad[j]

#print(MaxAngles)

MaxAngles_Starboard = MaxAngles
MaxAngles_Port = MaxAngles


