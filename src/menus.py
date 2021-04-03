import objects.primitives as prim
import search.greedy_solution as greedy
import search.heuristics as heur
import objects.data as dat
import search.genetic_algorithm as gen

from timeit import default_timer as timer


def pause():
    input("press any key to continue...")


def cooling_function():
    while True:
        print("-> Select Cooling Function")

        menu = {
            1: ["Exponential", heur.CoolingFunctions.exponential],
            2: ["Linear", heur.CoolingFunctions.linear],
            3: ["Quadratic", heur.CoolingFunctions.quadratic],
            4: ["Logarithmic", heur.CoolingFunctions.logarithmic]
        }

        choice = _process_choice(menu)
        if choice is not None:
            return choice


def _greedy():
    menu_header("Greedy Solution")
    start = timer()
    solution = greedy.greedy_solution(True)
    solution.update_internal()
    end_greedy = timer()
    print(repr(solution))
    print("Took:", (end_greedy - start), "seconds")

    return solution


def _naive():
    menu_header("Naive Solution")
    start = timer()
    solution = dat.initial_solution()
    solution.update_internal()
    end_greedy = timer()
    print(repr(solution))
    print("Took:", (end_greedy - start), "seconds")

    return solution


def _genetic():
    generations = 0
    while generations <= 0:
        generations = int(input("-> Number of Generations\n> "))

    initial_pop = 0
    while initial_pop <= 0:
        initial_pop = int(input("-> Initial Population\n> "))

    r_cross = 0
    while r_cross <= 0 or r_cross > 1:
        r_cross = float(input("-> Crossover Rate\n> "))

    r_mut = 0
    while r_mut <= 0 or r_mut > 1:
        r_mut = float(input("-> Mutation Rate\n> "))

    print("Starting Genetic Algorithm")
    print("Generations: {0}\nInitial Population: {1}\nCrossover Rate: {2}\nMutation Rate{3}"
          .format(generations, initial_pop, r_cross, r_mut))
    start = timer()
    best, best_score = gen.genetic_algorithm(generations, initial_pop, r_cross, r_mut)
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")


# --- Optimization Menus
def _sim_an(initial):
    iterations = 0
    while iterations <= 0:
        iterations = int(input("-> Number of Iterations for Simulated Annealing\n> "))

    function = cooling_function()

    print("Starting Simulated Annealing with", iterations, "iterations...")
    start = timer()
    best = heur.simulated_annealing(initial, function, iterations)
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")


def _it_sim_an(initial):
    iterations = 0
    while iterations <= 0:
        iterations = int(input("-> Number of Iterations to repeat Simulated Annealing\n> "))

    sa_iterations = 0
    while sa_iterations <= 0:
        sa_iterations = int(input("-> Number of Iterations for Simulated Annealing\n> "))

    function = cooling_function()

    print("Starting Iterative Simulated Annealing with", iterations, "iterations", "each with", sa_iterations, "iterations...")
    start = timer()
    best = heur.iterative_simulated_annealing(initial, function, iterations, sa_iterations)
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")


def _hill_climbing(initial):
    iterations = 0
    while iterations <= 0:
        iterations = int(input("-> Number of Iterations for Hill Climbing\n> "))

    print("Starting Hill Climbing with", iterations, "iterations...")
    start = timer()
    best = heur.hill_climbing(initial, iterations)
    end_greedy = timer()
    print(repr(best))
    print("Took:", (end_greedy - start), "seconds")
# -----


def menu_header(header: str):
    print()
    print(len(header)*"-")
    print(header.upper())
    print(len(header)*"-")
    print()


def _process_choice(menu):
    for k, v in menu.items():
        print("[{0}] {1}".format(k, v[0]))
    print()
    choice = int(input("> "))

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


def greedy_hill_climbing():
    path = select_input()
    if not path: return

    solution = _greedy()
    _hill_climbing(solution)
    pause()


def greedy_sim_an():
    path = select_input()
    if not path: return

    solution = _greedy()
    _sim_an(solution)
    pause()


def greedy_it_sim_an():
    path = select_input()
    if not path: return

    solution = _greedy()
    _it_sim_an(solution)
    pause()


def greedy_non_opt():
    path = select_input()
    if not path: return

    _greedy()
    pause()


def naive_hill_climbing():
    path = select_input()
    if not path: return

    solution = _naive()
    _hill_climbing(solution)
    pause()


def naive_sim_an():
    path = select_input()
    if not path: return

    solution = _naive()
    _sim_an(solution)
    pause()


def naive_it_sim_an():
    path = select_input()
    if not path: return

    solution = _naive()
    _it_sim_an(solution)
    pause()


def naive_non_opt():
    path = select_input()
    if not path: return

    _naive()
    pause()

def genetic():
    path = select_input()
    if not path: return

    _genetic()
    pause()


def main_menu():
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


def user_interface():
    menu_stack = [main_menu]
    while len(menu_stack) > 0:
        next_menu = menu_stack[0]()

        if next_menu is None:
            menu_stack.pop(0)
        else:
            menu_stack.insert(0, next_menu)

