import numpy as np

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

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):

    # Cree les nodes start et end
    node_initial = Node(None, start)
    node_initial.g = node_initial.h = node_initial.f = 0
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
            child.h = heuristic(child, node_final, current_node)
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

def heuristic(node_final, child, current_node):
    #  cost of the cheapest path from n to the goal  
    h = ((child.position[0] - node_final.position[0]) ** 2) + ((child.position[1] - node_final.position[1]) ** 2)
    return h

    # Add real heuristic function
    

def main():
    maze = np.zeros(shape=(200,120))     
    
    start = (5, 1)
    end = (100, 50)
    print("Initial: " + str(start))
    path = astar(maze, start, end)
    print("Path: " + str(path))
    print("Final: " + str(end))


if __name__ == '__main__':
main() 