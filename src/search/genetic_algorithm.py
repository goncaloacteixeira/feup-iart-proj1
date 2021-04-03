import concurrent.futures
import pandas as pd
import matplotlib.pyplot as plt

from objects.primitives import *
from numpy import random, mean
import search.greedy_solution as greed


def create_population(n_pop) -> list[Chromosome]:
    """
    Creates a random population using a non greedy algorithm

    :param n_pop: number of individuals (chromosomes)
    :return: list containing a population
    """
    population = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(n_pop):
            population.append(executor.submit(greed.greedy_solution, False))

    return list(map(lambda x: x.result(), population))


def best_individual(pop: list[Chromosome]) -> (Chromosome, float):
    """
    Calculates the best individual among a population
    :param pop: sample population (chromosomes)
    :return: best individual (highest score, including penalties)
    """
    current_best = (None, -9999)
    for chromosome in pop:
        score = chromosome.update_internal()
        if score > current_best[1]:
            current_best = chromosome, score
    return current_best


def selection(pop, scores, k=3) -> Chromosome:
    """
    Tournament Selection: chooses an individual and makes it "fight" with the rest
    of the population

    :param pop: sample population (chromosomes)
    :param scores: list with scores (evaluation function)
    :param k: number of tournament participants
    :return: the best chromosome
    """
    # first random selection
    selection_ix = random.randint(len(pop))
    for ix in random.randint(0, len(pop), k - 1):
        # check if better (e.g. perform a tournament)
        if scores[ix] > scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


def crossover(p1: Chromosome, p2: Chromosome, r_cross: float) -> list[Chromosome]:
    """
    Crossover operation between two chromosomes with a given rate

    :param p1: first chromosome
    :param p2: second chromosome
    :param r_cross: Crossover Rate (probabilistic)
    :return: two resulting chromosomes after the crossover operation
    """
    if random.random() <= r_cross:
        # ver tamanhos de ambos os cromossomas
        # escolher menor dos 2
        max_length = min(len(p1.genes), len(p2.genes))

        # escolher tamanho de 1 até o valor de cima
        size = random.randint(1, max_length) if  max_length > 1 else 1

        # escolher indice inicial de genes entre ind 0 e len-tamanho de cima
        g1_ind = random.randint(0, len(p1.genes) - size + 1)
        g2_ind = random.randint(0, len(p2.genes) - size + 1)

        # fazer a troca
        g1_genes = p1.genes[g1_ind:g1_ind + size]
        g2_genes = p2.genes[g2_ind:g2_ind + size]

        g1_drones = [gene.drone_id for gene in g1_genes]
        g2_drones = [gene.drone_id for gene in g2_genes]

        for i in range(g1_ind, g1_ind + size):
            p1.genes[i].drone_id = g2_drones[i - g1_ind]

        for i in range(g2_ind, g2_ind + size):
            p2.genes[i].drone_id = g1_drones[i - g2_ind]

        # To switch genes instead of drones
        # p1.genes[g1_ind:g1_ind+size] = g2_genes
        # p2.genes[g2_ind:g2_ind+size] = g1_genes

        return [p1, p2]
    return [p1, p2]


def mutation(c: Chromosome, r_mut) -> Chromosome:
    """
    Mutates a chromosome with a given rate

    :param c: chromosome to be mutated
    :param r_mut: mutation rate
    :return: mutated chromosome
    """
    if random.random() <= r_mut:
        new_c = c.mutate()
        return new_c
    return c


def genetic_algorithm(n_iter, n_pop, r_cross, r_mut):
    """
    Genetic Algorithm, with a given number of generations, a size for the initial population and the mutation
    and crossover rates

    :param n_iter: number of generations for the algorithm
    :param n_pop: number of individuals for the initial population
    :param r_cross: crossover rate [0.0, 1.0)
    :param r_mut: mutation rate [0.0, 1.0)
    :return: best individual among every generation
    """

    # initial population of random bitstring
    pop = create_population(n_pop)
    # keep track of best solution
    best, best_eval = best_individual(pop)

    data = {"generation": [], "mean": [], "best": []}
    scores = []

    # enumerate generations
    for gen in range(n_iter):
        # evaluate all candidates in the population
        scores = [c.update_internal() for c in pop]
        print("GEN ", gen + 1, "OF ", n_iter, "| MAX SCORE: ", str(max(scores)), " MEAN: ", mean(scores))
        # check for new best solution
        for i in range(n_pop):
            if scores[i] > best_eval and not pop[i].penalty:
                best, best_eval = pop[i], scores[i]
                print(">%d, new best f(%s) = %.3f" % (gen, repr(pop[i]), scores[i]))

        data['generation'].append(gen)
        data['best'].append(best_eval)
        data['mean'].append(mean(scores))

        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i + 1]
            # crossover and mutation
            for c in crossover(deepcopy(p1), deepcopy(p2), r_cross):
                # mutation
                new_c = mutation(c, r_mut)
                # store for next generation
                children.append(new_c)
        # replace population

        children = list(filter(lambda x: x.update_internal() > 0, children))
        ancestors = random.choice(range(n_pop), size=(n_pop-len(children)))
        pop = children + [pop[i] for i in ancestors]

    data['generation'].append(n_iter)
    data['best'].append(best_eval)
    data['mean'].append(mean(scores))

    df = pd.DataFrame(data=data)

    fig, ax = plt.subplots()

    df.plot(x='generation', y='best', ax=ax)
    df.plot(x='generation', y='mean', ax=ax)

    best_score = max(data['best'])
    xpos = data['best'].index(best_score)
    xmax = data['generation'][xpos]

    ax.annotate(str(best_score) + "(generation = " + str(xmax) + ")", xy=(xmax, best_score), xytext=(xmax, best_score + 5),
                arrowprops=dict(facecolor='black', shrink=0.05),
                )

    ax.set_ylim(min(data['mean']) - 10, 110)
    fig.set_size_inches(18.5, 11.5)
    ax.set_title('Genetic Algorithms')
    ax.set_ylabel('Score')

    plt.show()

    return best.clean(), best_eval
