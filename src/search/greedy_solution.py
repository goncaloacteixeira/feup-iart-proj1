from objects.primitives import *


def greedy_solution(use_best: bool = True):
    """
    Find a solution using a greedy algorithm, if the flag use_best is enabled the algorithm will use
    a slight less efficient method to calculate the solution (random), this is significantly faster
    and is used to create the initial population for the genetic algorithm

    :param use_best: flag to indicate if the method to be used is the extra greedy or the random
    :return: a solution for the problem
    """
    orders, warehouses = deepcopy(Problem.orders), deepcopy(Problem.warehouses)

    # initialize drone paths
    drone_path_list = {}
    for i in range(Problem.drones):
        drone_path_list[i] = DronePath(i, Problem.warehouses[0].position)

    chromosome = Chromosome(None, drone_path_list)

    orders_done = 0
    while not all_orders_complete(orders):
        for i, drone_path in drone_path_list.items():
            temp = best_shipment(drone_path, chromosome, orders, warehouses) if use_best else \
                   one_shipment(drone_path, chromosome, orders, warehouses)
            if temp < 0:
                break
            else:
                orders_done += temp
                # print("Orders Completed: ", orders_done, "/", len(orders))
    return chromosome


def best_shipment(drone_path: DronePath, chromosome: Chromosome, orders: list[Order], warehouses: list[Warehouse]) -> int:
    """
    Calculates the best shipment for a drone

    :param drone_path: the target drone's path
    :param chromosome: the target chromosome
    :param orders: a list of problem's orders
    :param warehouses: a list of problem's warehouses
    :return: the number of completed orders for this shipment
    """

    best = 0
    best_shipment = None

    for order in orders:
        if not order.complete():
            for warehouse in warehouses:
                shipment = Shipment(drone_path, order, warehouse)
                if shipment.has_products() and drone_path.turns + shipment.turns <= Problem.turns and shipment.score > best:
                    best, best_shipment = shipment.score, shipment
    if best_shipment is None:
        return -1

    order_complete = best_shipment.execute(chromosome)
    # print("Sent Shipment with Drone", drone_path.drone_id, ", order", best_shipment.order.id)
    return order_complete


def one_shipment(drone_path: DronePath, chromosome: Chromosome, orders: list[Order], warehouses: list[Warehouse]) -> int:
    """
    Essentially the same as the best_shipment method but the selection is done with randomness

    :param drone_path: the target drone's path
    :param chromosome: the target chromosome
    :param orders: a list of problem's orders
    :param warehouses: a list of problem's warehouses
    :return: the number of completed orders for this shipment
    """

    not_completed = [order for order in orders if not order.complete()]
    if not not_completed:
        return -1
    order = random.choice(not_completed)
    available_wh = [wh for wh in warehouses if wh.has_any_product(order.products)]
    warehouse = random.choice(available_wh)
    shipment = Shipment(drone_path, order, warehouse)
    order_complete = shipment.execute(chromosome)
    # print("Sent Shipment with Drone", drone_path.drone_id, ", order", shipment.order.id)
    return order_complete


def all_orders_complete(orders: list[prim.Order]) -> bool:
    """
    Checks if all orders on the provided argument are completed

    :param orders: list of orders to check
    :return: True if every order is complete, False otherwise
    """

    for order in orders:
        if not order.complete():
            return False
    return True
