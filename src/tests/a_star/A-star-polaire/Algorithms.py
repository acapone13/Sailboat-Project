import numpy as np
import matplotlib.pyplot as plt
import scipy as sci
from Queue import Queue
from Queue import PriorityQueue
#from speedPolarCalc import *

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def heuristic(a,b):

    (x1, y1) = a
    (x2, y2) = b

    if (x1 > x2 and y1 > y2) or (x1 < x2 and y1 > y2):
        h =  abs(x2 - x1) + abs(y2 - y1)
        return h
    #if (x1 > x2 and y1 <= y2) or (x1 < x2 and y1 <= y2):
        #return -1
    else:
        return -1


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal,next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far