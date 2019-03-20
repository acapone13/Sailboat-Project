class Node():
    #addapté pour notre projet: l'algo trouve le chemin le plus vite pour arriver à la destination
	#avec l'utilisation du A* initialement, le robot pars de la position 5,1
	#et il arrive à la position 5,8  
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0     # g eh a relacao entre a tua posicao e a posicao inicial
        self.h = 0	   # h eh a relacao entre a tua posicao e a posicao final
        self.f = 0	   # f eh a soma entre g e h. O movimento optara pela menor soma

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Cree les nodes start et end
    node_inicial = Node(None, start)
    node_inicial.g = node_inicial.h = node_inicial.f = 0
    node_final = Node(None, end)
    node_final.g = node_final.h = node_final.f = 0

    # Inicializa as listas open and closed (listas que no futuro serao empilhadas)
    open_list = []
    closed_list = []

    # Adiciona o node de start
    open_list.append(node_inicial)

    # Loop until you find the end
    while len(open_list) > 0:

        # Prendre le node actuel
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Il a trouvé l'objectif
        if current_node == node_final:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
		#for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
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
            child.g = current_node.g + 1
            child.h = ((child.position[0] - node_final.position[0]) ** 2) + ((child.position[1] - node_final.position[1]) ** 2)
            child.f = child.g + child.h

            # Child est déjà dans l'open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Ajoute le child dans l'open list
            open_list.append(child)


def main():
			#0  X1 2  3  4  5  6  7  X2 9
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   #0
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],   #1
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],   #2
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],   #3
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],   #4
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],   #Y
            [0, 1, 1, 0, 1, 1, 0, 0, 0, 0],   #6
            [0, 1, 1, 0, 1, 1, 0, 0, 0, 0],   #7
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],   #8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]   #9

    start = (5, 1)
    end = (5, 8)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()