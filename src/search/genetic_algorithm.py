from objects.primitives import *
from numpy import random


def create_population(n_pop) -> list[Chromosome]:
    pass


def best_individual(pop: list[Chromosome]) -> (Chromosome, float):
    pass

# tournament selection
def selection(pop, scores, k=3) -> Chromosome:
    # first random selection
    selection_ix = random.randint(len(pop))
    for ix in random.randint(0, len(pop), k-1):
        # check if better (e.g. perform a tournament)
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


def crossover(p1, p2, r_cross):
    pass


def mutation(c, r_mut) -> list[Chromosome]:
    pass


def genetic_algorithm(objective, n_iter, n_pop, r_cross, r_mut):
    # initial population of random bitstring
    pop = create_population(n_pop)
    # keep track of best solution
    best, best_eval = best_individual(pop)
    # enumerate generations
    for gen in range(n_iter):
        # evaluate all candidates in the population
        scores = [c.update_internal() for c in pop]
        # check for new best solution
        for i in range(n_pop):
            if scores[i] > best_eval:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))
        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                mutation(c, r_mut)
                # store for next generation
                children.append(c)
        # replace population
        pop = children
    return [best, best_eval]
