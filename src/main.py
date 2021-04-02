import objects.data as dat
import objects.mutations as mut
import objects.primitives as prim
import search.heuristics as heur

if __name__ == "__main__":
    prim.Problem.read_file("./input_data/demo_altered.in")

    chromosome = dat.initial_solution()
    chromosome.update_internal()
    print(chromosome)

    mut.join_genes(chromosome.genes)


    # supplies = {}
    # for i, gene in enumerate(chromossome.genes):
    #     if gene.demand < 0: continue
    #     if (gene.node, gene.product) not in supplies:
    #         supplies[(gene.node, gene.product)] = [(i, gene)]
    #     else:
    #         supplies[(gene.node, gene.product)].append((i, gene))
    #
    #
    # iterable = {k: v for (k, v) in supplies.items() if len(v) > 1}
    # for key, value in iterable:
    #     print(key)

    solution = heur.hill_climbing(chromosome, 3000)
    # solution = heur.iterative_simulated_annealing(chromosome, heur.CoolingFunctions.linear, 30, 100)

    # print(chromosome)
    # print("SCORE:", chromosome.update_internal())

    pass
