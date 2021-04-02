import objects.data as dat
import objects.mutations as mut
import objects.primitives as prim
import search.heuristics as heur
import search.greedy_solution as greed
import search.genetic_algorithm as genet

if __name__ == "__main__":
    prim.Problem.read_file("./input_data/demo_altered.in")

    chrom1 = greed.greedy_solution(False)
    chrom2 = greed.greedy_solution(False)

    print(chrom1)
    print("----")
    print(chrom2)

    # best, best_eval = genet.genetic_algorithm(50, 50, 0.1, 0.1)
    #
    # print("BEST: ", best_eval, "\nCHROMOSSOME:\n", best)

    pass
