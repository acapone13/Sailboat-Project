from Algorithms import *
from Graph import *
from Tools import *

"""def draw_square_grid_example():
    g = SquareGrid(30, 15)
    g.walls = DIAGRAM1_WALLS  # long list, [(21, 0), (21, 2), ...]
    draw_grid(g)"""

def a_star_search_example():
    came_from, cost_so_far = a_star_search(diagram4, (3, 4), (3, 18))
    #draw_grid(diagram4, width=3, point_to=came_from, start=(8, 4), goal=(3, 18))
    print()
    draw_grid(diagram4, width=3, number=cost_so_far, start=(3, 4), goal=(3, 18))


if __name__ == '__main__':
#    draw_square_grid_example()
    print('A Star')
    a_star_search_example()