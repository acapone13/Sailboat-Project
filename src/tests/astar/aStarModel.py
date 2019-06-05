import numpy as np
import time as tm
from polarplot import *
from scipy.spatial import distance

class Node():
    #addapté pour notre projet: l'algo trouve le chemin le plus vite pour arriver à la destination
	#avec l'utilisation du A* initialement, le robot pars de la position 5,1
	#et il arrive à la position 5,8  
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.anglePos = 0

        self.g = 0     # g est la relation entre la position et la position initiale
        self.h = 0	   # h est la relation la moins cher entre la position et la position finale
        self.f = 0	   # f est la somme entre g et h

        self.pp = polarPlot()   # Appel a la fonction pour interpoler les valeurs de vitesse avec angle et force du vent

        self.u = [0,0] # Sail angle and Rudder angle of the boat

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end, u, wind):
    #print(start, end, u, wind)
    #print(type(start),type(start),type(u),type(wind))
    # Cree les nodes start et end
    node_initial = Node(None, start)
    node_initial.g = node_initial.h = node_initial.f = 0
    #node_initial.u = [u[0], u[1]]
    node_final = Node(None, end)
    node_final.g = node_final.h = node_final.f = 0
    uAngle = [u[0], u[1]]

    # Initialization de les listes open and closed
    open_list = []
    closed_list = []

    # Ajoute le node start
    open_list.append(node_initial)

    # Loop jusqu'a trouver le bout
    while len(open_list) > 0:
        # tic = tm.clock()
        # Prendre le node actuel
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # toc = tm.clock()
        # print("Time 1: ", toc - tic)

        #print(len(open_list))

        # Pop le actuel off open list et ajoute à closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # tic = tm.clock()
        # Il a trouvé l'objectif
        if current_node == node_final:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            #print(closed_list)
            return path[::-1] # ça va retourner le chemin inverse

        # toc = tm.clock()
        # print("Time 2: ", toc - tic)

        # tic = tm.clock()
        # Gerer children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            # Trouver angles correspondantes au prochain position
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

            # Prendre position du node
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Certain que est dans le range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Certain que le chemin est possible
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Cree un nouveau node
            new_node = Node(current_node, node_position)
            new_node.anglePos = anglePos

            # Append les nodes
            children.append(new_node)
        
        # toc = tm.clock()
        # print("Time 3: ", toc - tic)

        # tic = tm.clock()
        # Loop dans les children
        for child in children:

            # Child est déjà dans le closed list
            nextChild = False
            for closed_child in closed_list:
                if child == closed_child:
                    nextChild = True
                    break
            if nextChild:
                continue

            #Cree les f, g, and h valeurs
            child.g = cost_of_path(current_node)
            child.h = heuristic(node_final, child, uAngle, wind)
            child.f = child.g + child.h

            # Child est déjà dans l'open list
            nextChild = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    nextChild = True
                    break
            if nextChild:
                continue

            

            # Ajoute le child dans l'open list
            open_list.append(child)
    
        # toc = tm.clock()
        # print("Time 4: ", toc - tic)

def cost_of_path(current_node):
    # cost of the path from the start node to n
    return current_node.g + 1

def heuristic(node_final, child, u, wind):
    #  cost of the cheapest path from n to the goal  
    cost = (((child.position[0] - node_final.position[0]) ** 2) ** 0.5)  + (((child.position[1] - node_final.position[1]) ** 2) ** 0.5)
    TWS = wind[0]
    """TWA = child.pp.getMaxTWA(TWS,abs(wind[1] - u[0]))
    child.pp.interpolate(TWS, TWA)
    boat_speed = child.pp.getBoatSpeed()
    boat_angle = child.pp.getBoatAngle()

    print(TWA)
    print(boat_angle,boat_speed)
    print(child.u)"""

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
        u[0] = child.pp.getBoatAngle()
    elif child.anglePos == 6:
        child.pp.getTWA(TWS, -120, -60)
        h = cost - child.pp.getBoatSpeed()
        u[0] = child.pp.getBoatAngle()
    elif child.anglePos == 7:
        child.pp.getTWA(TWS, -60, -30)
        h = cost - child.pp.getBoatSpeed()*2
        u[0] = child.pp.getBoatAngle()
    else: 
        h = cost
        u[0] = child.pp.getBoatAngle()
        
    """
    if TWA < 30 or TWA > 330:
        h = cost
        u[0] = boat_angle        
    elif (TWA >= 30 and TWA < 60) or (TWA >= 300 and TWA < 330):
        h = cost - boat_speed
        u[0] = boat_angle
    elif (TWA >= 60 and TWA < 90) or (TWA >= 270 and TWA < 300):
        h = cost - boat_speed
        u[0] = boat_angle
    elif (TWA >= 90 and TWA < 120) or (TWA >= 240 and TWA < 270):
        h = cost - boat_speed
        u[0] = boat_angle
    elif (TWA >= 120 and TWA < 150) or (TWA >= 210 and TWA < 240):
        h = cost - boat_speed
        u[0] = boat_angle
    else:
        h = cost - boat_speed
        u[0] = boat_angle"""
    #print(h)
    return round(h,4)

def longPathCalcul(xMazePos, yMazePos, objective, step):
    #print(xMazePos,yMazePos)
    dist = np.array([10000])
    dMin = 100
    x = 0
    y = 0
    for xPos in xMazePos:
        for yPos in yMazePos:
            d = np.sqrt((objective[0] - xPos)**2 + (objective[1] - yPos)**2)  
            dist = np.append(dist,d)
            if d < dMin:
                dMin = d
                x = xPos
                y = yPos

    return x,y,dMin

def main():
    maze = np.zeros(shape=(200,120)) # Simulator size (200,120)
    start = (5,1)  # Simulation map starting point
    # initPos = (0,5) # A* maze starting point
    # objective = (50,10) # Simulation map ending point
    # print(type(objective))
    end = (150,80) # A* maze ending point (changed after)
    wind = (8,0)
    u = (0,0)
    
    print("Initial: " + str(start))
    path = astar(maze, start, end, u, wind)
    path = np.asarray(list(path))
    print("Path: " + str(path.tolist()))
    print("Final: " + str(end), "\n")

    #speedCalculation
    #pp = polarPlot()
    #print()
    #print(pp.interpolate(17,10))

if __name__ == '__main__':
    main() 