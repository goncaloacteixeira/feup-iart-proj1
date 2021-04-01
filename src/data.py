from heuristics import simulated_annealing, hill_climbing, CoolingFunctions, iterative_simulated_annealing
from objects.primitives import *
from collections import Counter


def parse_file(filename) -> tuple[int, int, int, int, int, list[Warehouse], list[Order], list[Product]]:
    with open(filename, 'r') as file:
        # header
        n_rows, n_cols, n_drones, max_turns, max_payload = [int(x) for x in file.readline().split(" ")]

        # products
        n_products = int(file.readline())
        product_weights = list(map(int, file.readline().split(" ")))
        # to ensure the number of products corresponds to the actual read weights
        assert n_products == len(product_weights)
        products = [Product(i, weight) for i, weight in enumerate(product_weights)]

        # warehouses
        num_warehouses = int(file.readline())
        warehouses = []
        for i in range(num_warehouses):
            x, y = map(int, file.readline().split(" "))
            n_products_warehouse = list(map(int, file.readline().split(" ")))
            # to ensure the products are listed on the warehouse
            assert n_products == len(n_products_warehouse)
            # stores the warehouse products on a dict {Product -> quantity: int}
            warehouse_products = {product: n for product, n in zip(products, n_products_warehouse)}
            warehouse = Warehouse(i, Point(x, y), warehouse_products)
            warehouses.append(warehouse)

        # order
        order_list = []
        n_orders = int(file.readline())
        for i in range(n_orders):
            x, y = map(int, file.readline().split(" "))
            n_products_in_order = int(file.readline())
            order_products = list(map(int, file.readline().split(" ")))
            # to ensure the number of products in order actually corresponds to the number of products listed
            assert n_products_in_order == len(order_products)
            order_products = [products[x] for x in order_products]
            order = Order(i, Point(x, y), dict(Counter(order_products)))
            order_list.append(order)

    return n_rows, n_cols, n_drones, max_turns, max_payload, warehouses, order_list, products


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

    chromosome = initial_solution()

    print("Hill Climbing")
    best = hill_climbing(initial_input=chromosome, iterations=50)
    print(repr(best))

    # print("Simulated annealing")
    # best = iterative_simulated_annealing(chromosome, CoolingFunctions.linear, iterations=10, sa_iterations=50)
    # best = simulated_annealing(best, iterations=100, temp=50)
    # best = simulated_annealing(best, iterations=100, temp=50)
    # print(repr(best))
