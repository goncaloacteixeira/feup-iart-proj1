from src.objects.primitives import *
from src.data import *


def greedy_solution():

    # initialize drone paths
    drone_path_list = {}
    for i in range(Problem.drones):
        drone_path_list[i] = DronePath(i, Point(0, 0), [])

    chromosome = Chromosome(None, drone_path_list)

    while not all_orders_complete():
        attr_count = 0
        for i, drone_path in drone_path_list.items():
            attr_count += best_shipment(drone_path, chromosome)
            if attr_count == 0:
                break
    return chromosome


def best_shipment(drone_path: DronePath, chromosome):
    shipments: list[Shipment] = []
    for order in Problem.orders:
        if not order.complete():
            for warehouse in Problem.warehouses:
                shipment = Shipment(drone_path, order, warehouse)
                if shipment.has_products() and drone_path.turns + shipment.turns <= Problem.turns:
                    shipments.append(shipment)
    if len(shipments) == 0:
        return 0
    shipments = sorted(shipments, key=lambda shipment: -shipment.score)
    shipments[0].execute(chromosome)
    return 1


def all_orders_complete():
    for order in Problem.orders:
        if not order.complete():
            return False
    return True


if __name__ == "__main__":
    [Problem.rows, Problem.cols, Problem.drones, Problem.turns, Problem.payload, Problem.warehouses, Problem.orders,
     Problem.products] = parse_file("../input_data/demo_altered.in")

    chromosome = greedy_solution()

    print(chromosome)
    print("SCORE:", chromosome.update_internal())
