from objects.data import initial_solution
from objects.primitives import Problem
from search.heuristics import *

if __name__ == "__main__":
    Problem.read_file("./input_data/demo_altered.in")

    chromossome = initial_solution()

    supplies = {}
    for i, gene in enumerate(chromossome.genes):
        if gene.demand < 0: continue
        if (gene.node, gene.product) not in supplies:
            supplies[(gene.node, gene.product)] = [(i, gene)]
        else:
            supplies[(gene.node, gene.product)].append((i, gene))


    iterable = {k: v for (k, v) in supplies.items() if len(v) > 1}
    for key, value in iterable:
        print(key)

    # chromosome = initial_solution()
    #
    # solution = iterative_simulated_annealing(chromosome, CoolingFunctions.linear, 3, 10)

    # print(chromosome)
    # print("SCORE:", chromosome.update_internal())

    pass
