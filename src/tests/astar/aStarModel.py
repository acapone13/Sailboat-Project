import numpy as np
from polarplot import *

class Node():
    #addapté pour notre projet: l'algo trouve le chemin le plus vite pour arriver à la destination
	#avec l'utilisation du A* initialement, le robot pars de la position 5,1
	#et il arrive à la position 5,8  
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0     # g est la relation entre la position et la position initiale
        self.h = 0	   # h est la relation la moins cher entre la position et la position finale
        self.f = 0	   # f est la somme entre g et h

        self.pp = polarPlot()   # Appel a la fonction pour interpoler les valeurs de vitesse avec angle et force du vent

        self.u = [0,0] # Sail angle and Rudder angle of the boat

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end, u, wind):

    # Cree les nodes start et end
    node_initial = Node(None, start)
    node_initial.g = node_initial.h = node_initial.f = 0
    node_initial.u = [u[0], u[1]]
    node_final = Node(None, end)
    node_final.g = node_final.h = node_final.f = 0

    # Initialization de les listes open and closed
    open_list = []
    closed_list = []

    # Ajoute le node start
    open_list.append(node_initial)

    # Loop jusqu'a trouver le bout
    while len(open_list) > 0:

        # Prendre le node actuel
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop le actuel off open list et ajoute à closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Il a trouvé l'objectif
        if current_node == node_final:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # ça va retourner le chemin inverse

        # Gerer children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
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

            # Append les nodes
            children.append(new_node)

        # Loop dans les children
        for child in children:

            # Child est déjà dans l'open list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            #Cree les f, g, and h valeurs
            child.g = cost_of_path(current_node)
            child.h = heuristic(child, node_final, wind)
            child.f = child.g + child.h

            # Child est déjà dans l'open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Ajoute le child dans l'open list
            open_list.append(child)

def cost_of_path(current_node):
    # cost of the path from the start node to n
    return current_node.g + 1

def heuristic(node_final, child, wind):
    #  cost of the cheapest path from n to the goal  
    #h = (((child.position[0] - node_final.position[0]) ** 2) ** 0.5)  + (((child.position[1] - node_final.position[1]) ** 2) ** 0.5)

    TWS = wind[0]
    TWA = abs(wind[1] - child.u[0])
    child.pp.interpolate(TWS, TWA)
    boat_speed = child.pp.getBoatSpeed()
    boat_angle = child.pp.getBoatAngle()

    print(child.u[0])

    if TWA < 30:
        h = 1000
        child.u[0] = boat_angle
    elif TWA >= 30 and TWA < 60:
        h = boat_speed
        child.u[0] = boat_angle
    elif TWA >= 60 and TWA < 90:
        h = boat_speed
        child.u[0] = boat_angle
    elif TWA >= 90 and TWA < 120:
        h = boat_speed
        child.u[0] = boat_angle
    elif TWA >= 120 and TWA < 150:
        h = boat_speed
        child.u[0] = boat_angle
    else:
        h = boat_speed
        child.u[0] = boat_angle

    return h
    

def main():
    maze = np.zeros(shape=(200,120))     
    
    start = (5, 1)
    end = (5, 8)
    wind = (8,0)
    u = (10,0)
    print("Initial: " + str(start))
    path = astar(maze, start, end, u, wind)
    print("Path: " + str(path))
    print("Final: " + str(end))
    
    #speedCalculation
    #pp = polarPlot()
    #print()
    #print(pp.interpolate(17,10))


if __name__ == '__main__':
    main() 