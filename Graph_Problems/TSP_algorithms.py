import math
import random
from numpy.matrixlib.defmatrix import matrix
from data_structures.MinHeap import MinHeap
import numpy as np


def generate_matrix(coordinates) -> 'list[list]':
    ''' input a list of coordinates and generate a matrix of distances '''
    matrix = []
    for (x,y) in coordinates:
        row = []
        for (a,b) in coordinates:
            distance = math.sqrt( (x-a)**2 + (y-b)**2 )
            row.append(distance)
        matrix.append(row)
        
    return matrix 
        

class BranchAndBound():
    def __init__(self) -> None:
        pass
    
    def solve(self, matrix, n):
        self.matrix = matrix
        # add first element to list
        # calculate children
        # for each child, find lower bound
            # + if greater than current best, continue down branch
            # + else prune
        # return the best configuration and the cost
        
        optimal_config = None
        min_cost = math.inf
        Q = MinHeap()
        initial_config = [0]
        Q.insert(self.bounding_proc(initial_config), initial_config)
        while not Q.is_empty():
            lower_bound, config  = Q.delete_min().get()
            # print(config)
            if lower_bound < min_cost: 
                for p in self.branching_proc(config):
                    # if its a complete tour, compare cost to min
                    if len(p) == n:
                        cost_p = self.cost(p)
                        if cost_p < min_cost: optimal_config, min_cost = p, cost_p
                    # if its not, calculate the lower bound for this tour and add to Q
                    else: 
                        lb = self.bounding_proc(p)
                        if lb < min_cost: Q.insert(lb, p)
        return optimal_config, min_cost
    
    def bounding_proc(self, config) -> float:
        unconnected = [x for x in range(0,len(self.matrix)) if x not in config]
        cost = self.cost(config)
        for x in unconnected:
            min = math.inf
            row = self.matrix[x]
            for i,val in enumerate(row):
                if i not in config and val < min: min = val
            cost += min
        return cost 
    
    def branching_proc(self,config):
        branches = []
        for i in [x for x in range(0,len(self.matrix)) if x not in config]:
            b = list(config)
            b.append(i)
            branches.append(b)
        return branches
    
    def cost(self, config) -> float:
        i,q = 0,1
        cost = 0
        while q < len(config):
            u,v = config[i], config[q]
            # matrix is a numpy array, its more efficient
            cost += self.matrix[u][v]
            i += 1
            q += 1
        return cost            
    