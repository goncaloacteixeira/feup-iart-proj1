from math import exp, log
from random import randint
import pandas as pd
import matplotlib.pyplot as plt

from objects.primitives import Chromosome


class CoolingFunctions:
    @staticmethod
    def exponential(t0, iteration, _): return t0 * 0.8 ** iteration

    @staticmethod
    def logarithmic(t0, iteration, _): return t0 / (1 + log(1 + iteration))

    @staticmethod
    def linear(t0, iteration, max_iterations): return -iteration * t0 / max_iterations + t0 or 0.001

    @staticmethod
    def quadratic(t0, iteration, _): return t0 / (1 + iteration ** 2)


def plot_simulated_annealing(data):
    df = pd.DataFrame(data=data)

    fig, ax = plt.subplots()

    plt.figure(figsize=(10, 10), dpi=80)

    df.plot(x='iteration', y='current', ax=ax)
    df.plot(x='iteration', y='best', ax=ax)
    df.plot(x='iteration', y='temperature', ax=ax, secondary_y=True)

    best_score = max(data['best'])
    xpos = data['best'].index(best_score)
    xmax = data['iteration'][xpos]

    ax.annotate(str(best_score) + " (max)", xy=(xmax, best_score), xytext=(xmax, best_score + 5),
                arrowprops=dict(facecolor='black', shrink=0.05),
                )

    ax.set_ylim(min(data['current']) - 10, 110)

    plt.show()

    print("new plot - max:", best_score)


def hill_climbing(initial_input: Chromosome, iterations: int = 100) -> Chromosome:
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

    plt.ylim(0, 100)

    plt.show()

    return chromosome.clean()


def _simulated_annealing(initial_value: Chromosome, cooling_function, iterations: int = 50, temp: int = 100,
                        cumulative: int = 0, data=None):
    if data is None:
        data = {'best': [], 'current': [], 'iteration': [], 'temperature': []}

    best = initial_value
    best_score = best.update_internal()

    current, current_score = best, best_score

    data['best'].append(best_score)
    data['current'].append(current_score)
    data['iteration'].append(cumulative)
    data['temperature'].append(temp)

    # print("start score:", current_score)

    for i in range(1, iterations + 1):
        candidate = current.mutate()
        candidate_score = candidate.update_internal()
        # print("Candidate score:", candidate_score)
        if candidate_score > best_score:
            best, best_score = candidate, candidate_score
            # print("Found a better one, score:", best_score)
        diff = candidate_score - current_score
        t = cooling_function(temp, i, iterations)
        try:
            metropolis = exp(-diff / t)
        except OverflowError:
            metropolis = float('inf')

        if (diff < 0 or randint(0, 1) < metropolis) and candidate_score > 0:
            current, current_score = candidate, candidate_score

        data['best'].append(best_score)
        data['current'].append(current_score)
        data['iteration'].append(cumulative + i)
        data['temperature'].append(t)

    return best.clean()


def simulated_annealing(initial_value: Chromosome, cooling_function, iterations, temp: int = 100):
    data = {'best': [], 'current': [], 'iteration': [], 'temperature': []}
    best = _simulated_annealing(initial_value, cooling_function, iterations, temp, data=data)
    plot_simulated_annealing(data)

    return best


def iterative_simulated_annealing(initial_input, cooling_function, iterations: int = 3, sa_iterations: int = 100, temp: int = 100):
    data = {'best': [], 'current': [], 'iteration': [], 'temperature': []}
    for i in range(iterations):
        cumulative = i*sa_iterations

        initial_input = _simulated_annealing(initial_input, cooling_function, sa_iterations, temp, cumulative=cumulative, data=data)
        plot_simulated_annealing(data)

    return initial_input
