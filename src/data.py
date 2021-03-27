from objects.primitives import *
# from objects.constraints import *
from collections import Counter


def parse_file(filename) -> tuple[int, int, int, int, int, list[Warehouse], list[Order]]:
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

    return n_rows, n_cols, n_drones, max_turns, max_payload, warehouses, order_list


def deliverGenes(orders):
    list = []
    i = -1
    for order in orders:
        i += 1
        for product, quantity in order.products.items():
            remaining = quantity
            max_product = math.floor(problem.payload / product.weight)  # max products per drone
            drones_needed = math.ceil(quantity / max_product)

            for i in range(drones_needed - 1):
                remaining -= max_product
                list.append(Gene(None, -max_product, order, product))
            if remaining != 0:
                list.append(Gene(None, -remaining, order, product))

    return list


def calculate_product(warehouse_available, needed):
    if warehouse_available >= needed:
        available = warehouse_available - needed
        return available, 0
    else:
        still_need = needed - warehouse_available
        return 0, still_need


def initial_solution(problem):
    wh_copy = problem.warehouses.copy()
    chromosome = Chromosome([])
    drone = 0

    supplier_genes = deliverGenes(problem.orders)
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
                    if drone > problem.drones - 1:
                        drone = 0
                    break

    return chromosome


if __name__ == "__main__":
    problem = Problem(*parse_file("input_data/demo_altered.in"))

    chromosome = initial_solution(problem)
    print(chromosome)
    # print(check_turns(chromosome, problem))

    print("-----")
    # drone 1 path
    path = DronePath(1)
    previous_position = problem.warehouses[0].position

    for gene in chromosome.genes:
        if not chromosome.path_exists(gene.droneID):
            chromosome.add_path(gene.droneID)

        path = chromosome.get_path(gene.droneID)
        last_step = path.get_last_step()
        if last_step is None:
            previous_position = problem.warehouses[0].position
            previous_turns = 0
        else:
            previous_position = last_step.node.position
            previous_turns = last_step.turn

        gene.set_turns(previous_turns +
                       gene.node.position.distance(previous_position) +
                       1)
        path.add_step(gene)

    chromosome.print_solution()
