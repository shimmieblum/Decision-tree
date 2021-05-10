from math import radians
from Graph_Problems.TSP_algorithms import BranchAndBound, generate_matrix  
import random 
import time

            
if __name__ == '__main__':
    for i in range(1,20):
        solver = BranchAndBound()
        coords = [(random.randrange(1,100), random.randrange(1,100)) for _ in range(i)]
        matrix = generate_matrix(coords)
        # print(matrix)
        print(f'number of cities: {i}')
        s = time.time()
        print(solver.solve(matrix, len(matrix)))
        print(f'time taken: {round(time.time()-s, 2)}s')
        print('''
____________
''')