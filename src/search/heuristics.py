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


def plot_simulated_annealing(data: dict) -> None:
    """
    Plots the data acquired on the simulated annealing algorithm

    :param data: data containing iterations, best values and temperatures
    """

    df = pd.DataFrame(data=data)

    fig, ax = plt.subplots()

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
    fig.set_size_inches(18.5, 10.5)
    ax.set_title('Simulated Annealing')


def hill_climbing(initial_input: Chromosome, iterations: int = 100) -> Chromosome:
    """
    Hill Climbing Heuristic for a solution

    :param initial_input: the initial solution to be optimized
    :param iterations: number of max iterations for the algorithm
    :return: the optimized solution
    """

    chromosome = initial_input
    score = chromosome.update_internal()

    data = {'value': [score], 'iteration': [0]}

    for i in range(1, iterations + 1):
        candidate = chromosome.mutate()
        candidate_score = candidate.update_internal()
        if candidate_score >= score:
            chromosome, score = candidate, candidate_score

        data['value'].append(score)
        data['iteration'].append(i)

    plt.plot(data['iteration'], data['value'])
    plt.xlabel("Iteration")
    plt.ylabel("Value")
    plt.title("Hill Climbing")

    best_score = max(data['value'])
    xpos = data['value'].index(best_score)
    xmax = data['iteration'][xpos]

    plt.gca().annotate(str(best_score) + " (max)", xy=(xmax, best_score), xytext=(xmax, best_score + 5),
                       arrowprops=dict(facecolor='black', shrink=0.05),
                       )

    plt.gca().set_ylim(min(data['value']) - 10, 110)

    fig = plt.gcf()
    fig.set_size_inches(15.5, 10.5)

    plt.show()

    return chromosome.clean()


def _simulated_annealing(initial_value: Chromosome, cooling_function, iterations: int = 50, temp: int = 100,
                         cumulative: int = 0, data=None):
    """
    Simulated Annealing private method, the algorithm is implemented here, and it will collect the data to
    later display the plot.

    :param initial_value: initial solution to optimize
    :param cooling_function: cooling function to be used
    :param iterations: max iterations for the algorithm
    :param temp: initial temperature
    :param cumulative: cumulative iterations (used for iterative simulated annealing)
    :param data: data to be collected
    :return: the optimized solution
    """

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
    """
    Public method for the simulated annealing, it will run the algorithm and display a plot for the data collected
    afterwards

    :param initial_value: initial solution to optimize
    :param cooling_function: cooling function to be used
    :param iterations: max iterations for the algorithm
    :param temp: initial temperature
    :return: the optimized solution
    """

    data = {'best': [], 'current': [], 'iteration': [], 'temperature': []}
    best = _simulated_annealing(initial_value, cooling_function, iterations, temp, data=data)
    plot_simulated_annealing(data)
    plt.show()
    return best


def iterative_simulated_annealing(initial_input, cooling_function, iterations: int = 3, sa_iterations: int = 100,
                                  temp: int = 100):
    """
    'Iterative' Simulated Annealing, it will run the simulated annealing algorithm several times, trying to optimize
    the previous best solution

    :param initial_input: initial solution to optimize
    :param cooling_function: cooling function to be used
    :param iterations: max iterations for the algorithm
    :param sa_iterations: max iterations for each run of the simulated annealing
    :param temp: initial temperature
    :return: the optimized solution
    """

    data = {'best': [], 'current': [], 'iteration': [], 'temperature': []}
    for i in range(iterations):
        cumulative = i * sa_iterations
        initial_input = _simulated_annealing(initial_input, cooling_function, sa_iterations, temp,
                                             cumulative=cumulative, data=data)

    plot_simulated_annealing(data)
    plt.show()
    return initial_input
