import sys
from typing import Union
from timeit import default_timer as timer
import operator as op

import objects.primitives as prim
import search.greedy_solution as greedy
import search.heuristics as heur
import search.naive as dat
import search.genetic_algorithm as gen


def pause() -> None:
    input("press Enter to continue...")


def read_input(message: str,
               lower: (int, bool) = (0, False),      # Predefined lower bound is > 0
               upper: (int, bool) = (10000, False),  # Predefined upper bound is < 10000
               integer: bool = True) -> Union[int, float]:
    """ By default, accepts a integer input between ]0, 10000[ """

    lower_value, upper_value = lower[0], upper[0]
    value = lower[0]-1

    # if lower is inclusive -> checks lower than and not equal to keep in cycle
    # if lower not inclusive -> checks lower than or equal to keep in cycle
    comp1, l_bracket = (op.lt, "[") if lower[1] else (op.le, "]")
    # if upper is inclusive -> checks greater than and not equal to keep in cycle
    # if upper not inclusive -> checks greater than or equal to keep in cycle
    comp2, r_bracket = (op.gt, "]") if upper[1] else (op.ge, "[")

    while comp1(value, lower_value) or comp2(value, upper_value):
        try:
            value = int(input(message)) if integer else float(input(message))
            if value < lower_value or value > upper_value:
                print("Value must be in interval: {0}{1}, {2}{3}".format(l_bracket, lower_value, upper_value, r_bracket))
        except ValueError:
            print("You need to input a integer!")
        except Exception:
            print("\nBye bye")
            sys.exit()
    return value


def cooling_function():
    while True:
        print("-> Select Cooling Function")

        menu = {
            0: ["Exponential", heur.CoolingFunctions.exponential],
            1: ["Linear", heur.CoolingFunctions.linear],
            2: ["Quadratic", heur.CoolingFunctions.quadratic],
            3: ["Logarithmic", heur.CoolingFunctions.logarithmic]
        }

        choice = _process_choice(menu)
        if choice is not None:
            return choice


def _greedy() -> prim.Chromosome:
    menu_header("Greedy Solution")
    start = timer()
    solution = greedy.greedy_solution(True)
    solution.update_internal()
    end_greedy = timer()
    print(repr(solution))
    print("Took:", (end_greedy - start), "seconds")

    return solution


def _naive() -> prim.Chromosome:
    menu_header("Naive Solution")
    start = timer()
    solution = dat.naive_solution()
    solution.update_internal()
    end_greedy = timer()
    print(repr(solution))
    print("Took:", (end_greedy - start), "seconds")

    return solution


def _genetic() -> None:
    generations = read_input("-> Number of Generations\n> ")
    initial_pop = read_input("-> Initial Population\n> ")
    r_cross = read_input("-> Crossover Rate\n> ", upper=(1, True), integer=False)
    r_mut = read_input("-> Mutation Rate\n> ", upper=(1, True), integer=False)

    print("Starting Genetic Algorithm")
    start = timer()
    best, best_score = gen.genetic_algorithm(generations, initial_pop, r_cross, r_mut)
    print("Out of Genetic")
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")


# --- Optimization Menus
def _sim_an(initial):
    iterations = read_input("-> Number of Iterations for Simulated Annealing\n> ")

    function = cooling_function()

    print("Starting Simulated Annealing with", iterations, "iterations...")
    start = timer()
    best = heur.simulated_annealing(initial, function, iterations)
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")


def _it_sim_an(initial: prim.Chromosome) -> None:
    iterations = read_input("-> Number of Iterations to repeat Simulated Annealing\n> ")
    sa_iterations = read_input("-> Number of Iterations for Simulated Annealing\n> ")

    function = cooling_function()

    print("Starting Iterative Simulated Annealing with", iterations, "iterations", "each with", sa_iterations, "iterations...")
    start = timer()
    best = heur.iterative_simulated_annealing(initial, function, iterations, sa_iterations)
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")


def _hill_climbing(initial: prim.Chromosome) -> None:
    iterations = read_input("-> Number of Iterations for Hill Climbing\n> ",)

    print("Starting Hill Climbing with", iterations, "iterations...")
    start = timer()
    best = heur.hill_climbing(initial, iterations)
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")
# -----


def menu_header(header: str) -> None:
    print()
    print(len(header)*"-")
    print(header.upper())
    print(len(header)*"-")
    print()


def _process_choice(menu: dict[int, list]) -> str:
    for k, v in menu.items():
        print("[{0}] {1}".format(k, v[0]))
    print()
    choice = read_input("> ", (0, True), (len(menu), False))

    return menu[choice][1] if choice in menu.keys() else None


def select_input() -> bool:
    while True:
        menu_header("select data input")

        menu = {
            1: ["Busy Day", "./input_data/busy_day.in"],
            2: ["Mother of All Warehouses", "./input_data/mother_of_all_warehouses.in"],
            3: ["Redundancy", "./input_data/redundancy.in"],
            4: ["Demo", "./input_data/demo.in"],
            5: ["Demo Altered", "./input_data/demo_altered.in"],
            0: ["Cancel", None]
        }

        choice = _process_choice(menu)
        if choice is not None:
            print("Reading File...")
            prim.Problem.read_file(choice)
            print("Read File", choice)
            return True
        else:
            return False


def greedy_hill_climbing() -> None:
    path = select_input()
    if not path: return

    solution = _greedy()
    _hill_climbing(solution)
    pause()


def greedy_sim_an() -> None:
    path = select_input()
    if not path: return

    solution = _greedy()
    _sim_an(solution)
    pause()


def greedy_it_sim_an() -> None:
    path = select_input()
    if not path: return

    solution = _greedy()
    _it_sim_an(solution)
    pause()


def greedy_non_opt() -> None:
    path = select_input()
    if not path: return

    _greedy()
    pause()


def naive_hill_climbing() -> None:
    path = select_input()
    if not path: return

    solution = _naive()
    _hill_climbing(solution)
    pause()


def naive_sim_an() -> None:
    path = select_input()
    if not path: return

    solution = _naive()
    _sim_an(solution)
    pause()


def naive_it_sim_an() -> None:
    path = select_input()
    if not path: return

    solution = _naive()
    _it_sim_an(solution)
    pause()


def naive_non_opt() -> None:
    path = select_input()
    if not path: return

    _naive()
    pause()


def genetic() -> None:
    path = select_input()
    if not path: return

    _genetic()
    pause()


def main_menu() -> str:
    while True:
        menu_header("Drone Delivery Google Hash Code")

        menu = {
            1: ["Greedy Solution - Hill Climbing", greedy_hill_climbing],
            2: ["Greedy Solution - Simulated Annealing", greedy_sim_an],
            3: ["Greedy Solution - Iterative Simulated Annealing", greedy_it_sim_an],
            4: ["Greedy Solution - Non-Optimized", greedy_non_opt],
            5: ["Naive Solution - Hill Climbing", naive_hill_climbing],
            6: ["Naive Solution - Simulated Annealing", naive_sim_an],
            7: ["Naive Solution - Iterative Simulated Annealing", naive_it_sim_an],
            8: ["Naive Solution - Non-Optimized", naive_non_opt],
            9: ["Genetic Algorithms", genetic],
            0: ["Exit", exit]
        }

        choice = _process_choice(menu)
        if choice is not None:
            return choice


def user_interface() -> None:
    menu_stack = [main_menu]
    while len(menu_stack) > 0:
        next_menu = menu_stack[0]()

        if next_menu is None:
            menu_stack.pop(0)
        else:
            menu_stack.insert(0, next_menu)
