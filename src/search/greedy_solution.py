from objects.primitives import *


def greedy_solution():
    orders, warehouses = Problem.orders.copy(), Problem.warehouses.copy()

    # initialize drone paths
    drone_path_list = {}
    for i in range(Problem.drones):
        drone_path_list[i] = DronePath(i, Problem.warehouses[0].position)

    chromosome = Chromosome(None, drone_path_list)

    orders_done = 0
    while not all_orders_complete():
        for i, drone_path in drone_path_list.items():
            temp = best_shipment(drone_path, chromosome, orders, warehouses)
            if temp < 0:
                break
            else:
                orders_done += temp
                print("Orders Completed: ", orders_done, "/", len(orders))
    return chromosome


def best_shipment(drone_path: DronePath, chromosome: Chromosome, orders: list[Order], warehouses: list[Warehouse]) -> int:
    shipments: list[Shipment] = []

    for order in orders:
        if not order.complete():
            for warehouse in warehouses:
                shipment = Shipment(drone_path, order, warehouse)
                if shipment.has_products() and drone_path.turns + shipment.turns <= Problem.turns:
                    shipments.append(shipment)
    if len(shipments) == 0:
        return -1
    shipments = sorted(shipments, key=lambda shipment: -shipment.score)
    order_complete = shipments[0].execute(chromosome)
    print("Sent Shipment with Drone", drone_path.drone_id, ", order", shipments[0].order.id)
    return order_complete


def all_orders_complete():
    for order in Problem.orders:
        if not order.complete():
            return False
    return True


if __name__ == "__main__":
    Problem.read_file("../input_data/redundancy.in")

    chromosome = greedy_solution()

    print(chromosome)
    print("SCORE:", chromosome.update_internal())
