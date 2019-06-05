from AI import IAI
import numpy as np 
import scipy as sci

class Astar(IAI):
    """
    Module used to implement astar from AI interface
    """

    def astar(maze, start, end, u, wind):
        # Creates the start and end node
        node_initial = Node(None, start)
        node_initial.g = node_initial.h = node_initial.f = 0
        node_final = Node(None, end)
        node_final.g = node_final.h = node_final.f = 0
        uAngle = [u[0], u[1]]

        # Initialization of open and closed lists
        open_list = []
        closed_list = []

        # Adds start node
        open_list.append(node_initial)

        # Loop until finding the target
        while len(open_list) > 0:
            # Takes current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop le current node from open list and adds it to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # The objective was found
            if current_node == node_final:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Returns the inverse way

            # Manage Children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
                # Finds the angles for the next position
                if new_position == (0,1):
                    anglePos = 0
                elif new_position == (1, 1):
                    anglePos = 1
                elif new_position == (1, 0):
                    anglePos = 2
                elif new_position == (1, -1):
                    anglePos = 3
                elif new_position == (0, -1):
                    anglePos = 4
                elif new_position == (-1, -1):
                    anglePos = 5
                elif new_position == (-1, 1):
                    anglePos = 6
                else:
                    anglePos = 7

                # Gets node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Verifies the position is inside the range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue

                # Verifies the way is possible
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Creates a new node
                new_node = Node(current_node, node_position)
                new_node.anglePos = anglePos

                # Append nodes
                children.append(new_node)

            # Loop inside children list
            for child in children:

                # Child is already in closed list
                nextChild = False
                for closed_child in closed_list:
                    if child == closed_child:
                        nextChild = True
                        break
                if nextChild:
                    continue

                # Creates g, h and f values
                child.g = cost_of_path(current_node)
                child.h = heuristic(node_final, child, uAngle, wind)
                child.f = child.g + child.h

                # Child is already at open list
                nextChild = False
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        nextChild = True
                        break
                if nextChild:
                    continue

                # Adds the child to open list
                open_list.append(child)

    def cost_of_path(current_node):
        # cost of the path from the start node to n
        return current_node.g + 1

    def heuristic(node_final, child, u, wind):
        #  cost of the cheapest path from n to the goal  
        cost = (((child.position[0] - node_final.position[0]) ** 2) ** 0.5)  + (((child.position[1] - node_final.position[1]) ** 2) ** 0.5)
        TWS = wind[0]

        if child.anglePos == 0:
            child.pp.getTWA(TWS,-30, 30)
            h = cost
            u[0] = child.pp.getBoatAngle()
        elif child.anglePos == 1:
            child.pp.getTWA(TWS, 30, 60)
            h = cost - child.pp.getBoatSpeed()*2
            u[0] = child.pp.getBoatAngle()
        elif child.anglePos == 2:
            child.pp.getTWA(TWS, 60, 120)
            h = cost - child.pp.getBoatSpeed()
            u[0] = child.pp.getBoatAngle()
        elif child.anglePos == 3:
            child.pp.getTWA(TWS, 120, 150)
            h = cost - child.pp.getBoatSpeed()*2
            u[0] = child.pp.getBoatAngle()
        elif child.anglePos == 4:
            child.pp.getTWA(TWS, 150, -150)
            h = cost
            u[0] = child.pp.getBoatAngle()
        elif child.anglePos == 5:
            child.pp.getTWA(TWS, -150, -120)
            h = cost - child.pp.getBoatSpeed()*2
            u[0] = -child.pp.getBoatAngle()
        elif child.anglePos == 6:
            child.pp.getTWA(TWS, -120, -60)
            h = cost - child.pp.getBoatSpeed()
            u[0] = -child.pp.getBoatAngle()
        elif child.anglePos == 7:
            child.pp.getTWA(TWS, -60, -30)
            h = cost - child.pp.getBoatSpeed()*2
            u[0] = -child.pp.getBoatAngle()
        else: 
            h = cost
            u[0] = child.pp.getBoatAngle()

        #print(h)
        return round(h,4)

    def step(self, params):
        raise NotImplementedError
        
    def log(self, message):
        print(message)


class Node(): 
    # The algorithm finds the fastest way to reach our goal with A*, initially the robot starts at the position (5,1)
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.anglePos = 0

        self.g = 0     # g is the relation between the current position and the initial position
        self.h = 0	   # h is the cheapest relation between the current position and the final position, takes also into consideration polar plot values
        self.f = 0	   # f is the sum between g and h

        self.pp = polarPlot()   # Creates polarPlot class that allows to interpolate speed and angle values from the boat

        self.u = [0,0] # Sail angle and Rudder angle of the boat

    def __eq__(self, other):
        return self.position == other.position

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
            self.boat_angle = 45

        self.interpolate(speed,self.boat_angle)