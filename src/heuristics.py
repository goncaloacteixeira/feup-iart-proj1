from math import exp, log
from random import randint
import pandas as pd
import matplotlib.pyplot as plt

from objects.primitives import Chromosome


class CoolingFunctions:
    @staticmethod
    def exponential(t0, iteration): return t0 * 0.8 ** iteration
    @staticmethod
    def logarithmic(t0, iteration): return t0 / (1 + log(1 + iteration))
    @staticmethod
    def linear(t0, iteration): return t0 / (1 + iteration)
    @staticmethod
    def quadratic(t0, iteration): return t0 / (1 + iteration ** 2)


def hill_climbing(initial_input, iterations: int = 100):
    chromosome = initial_input
    score = chromosome.update_internal()

    data = {'value': [score], 'iteration': [0]}

    for i in range(1, iterations + 1):
        candidate = chromosome.mutate()
        candidate_score = candidate.update_internal()
        if candidate_score >= score:
            chromosome, score = candidate, candidate_score
            print("Found a better one, score:", score)

        data['value'].append(score)
        data['iteration'].append(i)

    plt.plot(data['iteration'], data['value'])
    plt.xlabel("Iteration")
    plt.ylabel("Value")
    plt.title("Hill Climbing")

    plt.show()

    return chromosome


def simulated_annealing(initial_value: Chromosome, cooling_function, iterations: int = 50, temp: int = 100):
    best = initial_value
    best_score = best.update_internal()

    current, current_score = best, best_score

    data = {'best': [best_score], 'iteration': [0], 'current': [current_score], 'temperature': [temp]}

    # print("start score:", current_score)

    for i in range(1, iterations + 1):
        candidate = current.mutate()
        candidate_score = candidate.update_internal()
        # print("Candidate score:", candidate_score)
        if candidate_score > best_score:
            best, best_score = candidate, candidate_score
            # print("Found a better one, score:", best_score)
        diff = candidate_score - current_score
        t = cooling_function(temp, i)
        try:
            metropolis = exp(-diff / t)
        except OverflowError:
            metropolis = float('inf')

        if diff < 0 or randint(0, 1) < metropolis:
            current, current_score = candidate, candidate_score

        print(i)
        data['best'].append(best_score)
        data['current'].append(current_score)
        data['iteration'].append(i)
        data['temperature'].append(t)

    df = pd.DataFrame(data=data)

    fig, ax = plt.subplots()

    df.plot(x='iteration', y='current', ax=ax)
    df.plot(x='iteration', y='best', ax=ax)
    df.plot(x='iteration', y='temperature', ax=ax, secondary_y=True)

    xpos = data['best'].index(best_score)
    xmax = data['iteration'][xpos]

    ax.annotate(str(best_score) + " (max)", xy=(xmax, best_score), xytext=(xmax, best_score + 5),
                arrowprops=dict(facecolor='black', shrink=0.05),
                )

    ax.set_ylim(min(data['current']) - 10, 110)

    plt.show()

    return best


def iterative_simulated_annealing(initial_input, iterations: int = 3, sa_iterations: int = 100, temp: int = 100):
    for i in range(iterations):
        initial_input = simulated_annealing(initial_input, sa_iterations, temp)
    return initial_input
