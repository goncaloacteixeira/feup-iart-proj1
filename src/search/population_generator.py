from functools import cache
from data import *
from search.Utils import *
import random
import copy
from datetime import datetime


def generate_population(deliver_genes, max_depth=100, max_population=20):
    root = Node(Chromosome())
    root.warehouses = Problem.warehouses
    root.deliver_genes = deliver_genes

    solutions = []
    stack = [root]
    tree = Tree(root)

    visited = []
    depth = 1
    while depth != max_depth:
        new_stack = []
        for s in stack:
            if s.info not in visited:
                expanded = expand(s)
                for new_node in expanded:
                    if is_goal(new_node, len(deliver_genes)):
                        solutions.append(new_node.info)
                        visited.append(new_node.info)
                        if len(solutions) >= max_population:
                            return solutions
                    else:
                        new_stack.append(new_node)
                        tree.add_node(new_node)
                        s.add_edge(new_node, 1)
                visited.append(s.info)

        stack = new_stack
        depth += 1

    return solutions


@cache
def expand(node: Node):
    expanded = []

    while len(expanded) != 2:
        random.seed(datetime.now().second.real)

        new_node = copy.deepcopy(node)

        rand = random.randint(0, 1)

        if rand == 0:  # supply
            warehouse = new_node.warehouses[random.randint(0, len(new_node.warehouses) - 1)]
            product = random.choice(list(warehouse.products.keys()))

            if warehouse.products[product] == 0:
                continue

            quantity = random.randint(1, warehouse.products[product])
            warehouse.products.update({product: warehouse.products[product] - quantity})

            new_gene = Gene(drone_id=random.randint(0, Problem.drones - 1), demand=quantity, node=warehouse,
                            product=product)
            new_node.info.add_gene(new_gene)
            new_node.info.update_internal()
            if new_node.info.penalty == 0:
                expanded.append(new_node)

        else:  # deliver
            deliver_gene = new_node.deliver_genes.pop(random.randint(0, len(new_node.deliver_genes) - 1))
            deliver_gene.set_drone(random.randint(0, Problem.drones - 1))

            new_node.info.add_gene(deliver_gene)
            new_node.info.update_internal()
            if new_node.info.penalty == 0:
                new_node.supplies += 1
                expanded.append(new_node)

    return remove_dups(tuple(expanded))


@cache
def remove_dups(nodes):
    new_nodes = []
    visited = []
    for node in nodes:
        if node.info not in visited:
            visited.append(node.info)
            new_nodes.append(node)
    return new_nodes


if __name__ == "__main__":
    [Problem.rows, Problem.cols, Problem.drones, Problem.turns, Problem.payload, Problem.warehouses, Problem.orders,
     Problem.products] = parse_file("../input_data/demo_altered.in")

    deliver_genes = deliverGenes(Problem.orders)

    population = []

    while len(population) < 20:
        for solution in generate_population(deliver_genes, 30, 1):
            population.append(solution)
            print(repr(solution))
            print(solution)
            print()

