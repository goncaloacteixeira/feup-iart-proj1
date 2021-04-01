from src.objects.primitives import *
from math import exp
from random import randint


def deliverGenes(orders) -> list[Gene]:
    list = []
    i = -1
    for order in orders:
        i += 1
        for product, quantity in order.products.items():
            remaining = quantity
            max_product = math.floor(Problem.payload / product.weight)  # max products per drone
            drones_needed = math.ceil(quantity / max_product)

            for i in range(drones_needed - 1):
                remaining -= max_product
                list.append(Gene(None, -max_product, order, product))
            if remaining != 0:
                list.append(Gene(None, -remaining, order, product))

    return list


def calculate_product(warehouse_available, needed) -> tuple[int, int]:
    if warehouse_available >= needed:
        available = warehouse_available - needed
        return available, 0
    else:
        still_need = needed - warehouse_available
        return 0, still_need


def initial_solution() -> Chromosome:
    wh_copy = Problem.warehouses.copy()
    chromosome = Chromosome()
    drone = 0

    supplier_genes = deliverGenes(Problem.orders)
    for gene in supplier_genes:
        remaining_product = abs(gene.demand)  # demand product
        for warehouse in wh_copy:
            if warehouse.products.get(gene.product) is not None:
                wh_quantity, needed = calculate_product(warehouse.products.get(gene.product), remaining_product)
                if wh_quantity < warehouse.products.get(gene.product):
                    chromosome.add_gene(
                        Gene(drone, remaining_product - needed, warehouse, gene.product))  # add gene with pick up

                    warehouse.products.update({gene.product: wh_quantity})  # updates warehouse product
                    remaining_product = needed  # decrement demand product
                if remaining_product == 0:  # when demand is 0 we can add gene corresponding to delivery
                    gene.set_drone(drone)
                    chromosome.add_gene(gene)
                    drone += 1
                    if drone > Problem.drones - 1:
                        drone = 0
                    break
    return chromosome


if __name__ == "__main__":
    [Problem.rows, Problem.cols, Problem.drones, Problem.turns, Problem.payload, Problem.warehouses, Problem.orders,
     Problem.products] = parse_file("input_data/mother_of_all_warehouses.in")

    # chromosome = initial_solution()
    # print(chromosome)
    # chromosome.update_internal()
    #
    # print(" ----- ")
    #
    # print("SCORE ", chromosome.penalty)

    # print("Hill Climbing")
    # best = hill_climbing(iterations=1000)
    # print(repr(best))

    print("Simulated annealing")
    best = simulated_annealing(iterations=100, temp=50)
    best = simulated_annealing(best, iterations=100, temp=50)
    best = simulated_annealing(best, iterations=100, temp=50)

    print(repr(best))
