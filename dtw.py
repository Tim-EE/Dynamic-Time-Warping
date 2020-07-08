# This class can be used to perform dynamic time warping (DTW) on two signals.

import numpy as np
import matplotlib.pyplot as plt
import math

class DTW:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.accumulated_cost = -1
        self.distanceMatrix = -1
        self.paths = -1
        self.cost = -1
        self.dtwDistance = -1

    def run(self):
        # Generate the distance matrix for points withiin the signals
        self.distanceMatrix = create_distance_matrix(self.x,self.y)
        # calculate the cost matrix
        self.accumulated_cost = self.calculate_cost_matrix()
        # Backtracking and finding the optimal warp path
        self.paths,self.cost = path_cost(self.x, self.y, self.accumulated_cost, self.distanceMatrix)
        # get the optimal path (lowest cost)
        self.path_x = [point[0] for point in self.paths]
        self.path_y = [point[1] for point in self.paths]

    def print_warping(self):
        plt.plot(self.x, 'bo-' ,label='x')
        plt.plot(self.y, 'g^-', label = 'y')
        plt.legend();
        for [map_x, map_y] in self.paths:
            plt.plot([map_x, map_y], [self.x[map_x], self.y[map_y]], 'r', linewidth=2)

    def distance_cost_plot(self):
        if self.distanceMatrix == None: return

        im = plt.imshow(self.distanceMatrix, interpolation='nearest', cmap='Reds')
        plt.gca().invert_yaxis()
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid()
        plt.colorbar();
        plt.plot(self.path_x, self.path_y, linewidth=4)


    def calculate_cost_matrix(self):
        accumulated_cost = np.zeros((len(self.distanceMatrix), len(self.distanceMatrix[0])))
        accumulated_cost[0,0] = self.distanceMatrix[0,0]

        # calculate cost along X
        for i in range(1, len(self.x)):
            accumulated_cost[0,i] = self.distanceMatrix[0,i] + accumulated_cost[0, i-1]

        # calculate cost along Y
        for i in range(1, len(self.y)):
            accumulated_cost[i,0] = self.distanceMatrix[i, 0] + accumulated_cost[i-1, 0]

        # calculate all other costs
        for i in range(1, len(self.y)):
            for j in range(1, len(self.x)):
                accumulated_cost[i, j] = min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]) + self.distanceMatrix[i, j]

        return accumulated_cost


def plot_signals(x,y,save_file_as=None):
    fig, ax = plt.subplots()
    n = np.arange(0,len(x))
    ax.set(xlabel='sample', ylabel='signal value',
           title='')
    ax.grid()

    ax.plot(n, x)
    ax.plot(n, y)

    if save_file_as == None:
        plt.show()
    else:
        fig.savefig(save_file_as)


def create_distance_matrix(x,y):
    # initialize distance matrix entries to 0
    distanceMatrix = np.zeros((len(y), len(x)))
    for i in range(len(y)):
        for j in range(len(x)):
            distanceMatrix[i,j] = ((x[j] - y[i]) ** 2) ** 0.5

    return distanceMatrix



def path_cost(x, y, accumulated_cost, distances):
    path = [[len(x)-1, len(y)-1]]

    i = len(y)-1
    j = len(x)-1
    while i > 0 and j > 0:
        if i==0:
            j -= 1
        elif j==0:
            i -= 1
        else:
            if accumulated_cost[i-1, j] == min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]):
                i -= 1
            elif accumulated_cost[i, j-1] == min(accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]):
                j -= 1
            else:
                i -= 1
                j -= 1
        path.append([j, i])
    path.append([0,0])

    cost = 0
    for [y, x] in path:
        cost = cost + distances[x, y]
    return path, cost
