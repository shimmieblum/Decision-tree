import math

class BranchAndBound():
    def __init__(self) -> None:
        pass
    
    def solve(matrix) -> tuple(list, int):
        # add first element to list
        # calculate children
        # for each child, find lower bound
            # + if greater than current best, continue down branch
            # + else prune
        # return the best configuration
        
        optimal_config = None
        lowest_cost = math.inf
        Q =  