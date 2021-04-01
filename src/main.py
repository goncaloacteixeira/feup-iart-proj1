from objects.data import initial_solution
from objects.primitives import Problem
from search.heuristics import *

if __name__ == "__main__":
    Problem.read_file("./input_data/redundancy.in")

    chromosome = initial_solution()

    solution = iterative_simulated_annealing(chromosome, CoolingFunctions.linear, 3, 10)

    # print(chromosome)
    # print("SCORE:", chromosome.update_internal())

    pass
