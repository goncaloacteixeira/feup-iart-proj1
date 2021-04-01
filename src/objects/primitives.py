from __future__ import annotations
import math
from abc import ABC, abstractmethod
from typing import Union
from collections import Counter

from objects.mutations import *
from search.constraints import *


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "[POINT] X={x} Y={y}".format(x=self.x, y=self.y)

    def distance(self, point: 'Point') -> int:
        return math.ceil(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2))


class Product:
    def __init__(self, id: int, weight: int):
        self.id = id
        self.weight = weight

    def __str__(self) -> str:
        return "[PRODUCT {id}] - weight={weight}".format(id=self.id, weight=self.weight)


class Spot(ABC):
    @abstractmethod
    def __init__(self, id: int, position: Point, products: dict):
        self.id = id
        self.position = position
        self.products = products

    def add_products(self, products: dict):
        for product, quantity in products.items():
            if product in self.products:
                self.products[product] += quantity
            else:
                self.products[product] = quantity

    def remove_products(self, products: dict):
        for product, quantity in products.items():
            self.products[product] -= quantity
            if self.products[product] == 0:
                self.products.pop(product)


class Warehouse(Spot):
    def __init__(self, id: int, position: Point, products: dict):
        super().__init__(id, position, products)

    def __str__(self) -> str:
        products = ""
        for product, amount in self.products.items():
            products += str(product) + " amount=" + str(amount) + "\n"
        return "[WAREHOUSE {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)


class Order(Spot):
    def __init__(self, id: int, position: Point, products: dict):
        super().__init__(id, position, products)
        self.product_weight = sum(p.weight * q for p, q in self.products.items())

    def __str__(self) -> str:
        products = ""
        for product, quantity in self.products.items():
            products += str(product) + " quantity=" + str(quantity) + "\n"
        return "[ORDER {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)

    def complete(self):
        return not self.products


class Problem:
    """ Static Class to hold info about the problem"""
    rows: int = None
    cols: int = None
    drones: int = None
    turns: int = None
    payload: int = None
    warehouses: list[Warehouse] = None
    orders: list[Order] = None
    products: list[Product] = None

    @staticmethod
    def calculate_points(turn: int) -> int:
        return math.ceil(((Problem.turns - turn) / Problem.turns) * 100)

    # "../input_data/redundancy.in"
    @staticmethod
    def read_file(file_path: str):
        [Problem.rows, Problem.cols, Problem.drones, Problem.turns, Problem.payload, Problem.warehouses, Problem.orders,
         Problem.products] = Problem.parse_file(file_path)

    @staticmethod
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


class Gene:
    def __init__(self, drone_id: Union[int, None], demand: int, node: Spot, product: Product, turn: int = None):
        self.droneID = drone_id
        self.demand = demand
        self.node = node
        self.product = product
        self.turn = turn
        self.penalty = 0

    def __str__(self) -> str:
        return "[ {droneID} | {demand} | {productID} | {node} | {turns} | {penalty} ]".format(droneID=self.droneID,
                                                                                              demand=self.demand,
                                                                                              node=self.node.id,
                                                                                              productID=self.product.id,
                                                                                              turns=self.turn,
                                                                                              penalty=self.penalty)

    def set_drone(self, drone: int) -> None:
        self.droneID = drone

    def set_turns(self, turns: int) -> None:
        self.turn = turns

    def __eq__(self, o: Gene) -> bool:
        return self.droneID == o.droneID and self.demand == o.demand and self.node.id == o.node.id and self.product.id == o.product.id and self.turn == o.turn

    def __hash__(self) -> int:
        return super().__hash__()


class DronePath:
    def __init__(self, drone_id: int, current_position: Point = Point(0, 0), steps: list[Gene] = None):
        if steps is None:
            steps = []
        self.drone_id = drone_id
        self.steps = steps
        self.shipments = []
        self.current_position = current_position
        self.turns = 0

    def __str__(self) -> str:
        print("DRONE ", self.drone_id)
        [print(str(gene)) for gene in self.steps]
        return ""

    def get_last_step(self) -> Union[Gene, None]:
        try:
            return self.steps[-1]
        except IndexError:  # if steps = []
            return None

    def add_step(self, gene: Gene):
        self.steps.append(gene)

    def set_position(self, position: Point):
        self.current_position = position

    def add_shipment(self, shipment):
        self.shipments.append(shipment)

    def add_turns(self, turns):
        self.turns += turns


class OrderPath:
    def __init__(self, order: Order, steps: list[Gene] = None, score: int = 0):
        if steps is None:
            steps = []
        self.order = order
        self.steps = steps
        self.score = score  # calculated score for this order

    def __str__(self) -> str:
        print("ORDER ", self.order.id)
        [print(str(gene)) for gene in self.steps]
        return ""

    def add_step(self, gene: Gene) -> None:
        self.steps.append(gene)

    def update_score(self) -> int:
        maximum = max(gene.turn for gene in self.steps)
        self.score = Problem.calculate_points(maximum)
        return self.score


class Chromosome:
    def __init__(self, genes: list[Gene] = None, solution: dict[int, DronePath] = None,
                 orders: dict[int, OrderPath] = None, score: int = 0):
        if orders is None: orders = {}
        if genes is None: genes = []
        if solution is None: solution = {}
        self.genes = genes
        self.solution = solution
        self.orders = orders
        self.score = score
        self.penalty = 0

    def __str__(self) -> str:
        return "\n".join([str(gene) for gene in self.genes])

    def __repr__(self) -> str:
        return "[Chromosome] Genes: {genes} | Penalty: {penalty} | Score: {score}".format(genes=len(self.genes),
                                                                                          penalty=self.penalty,
                                                                                          score=self.score)

    def add_gene(self, gene: Gene) -> None:
        self.genes.append(gene)

    def print_solution(self):
        for key, value in self.solution.items():
            print(value)

    def print_orders(self):
        for key, value in self.orders.items():
            print(value)

    def update_internal(self) -> float:
        """ Updates Solution, orders and value of this chromosome """
        self.penalty = 0
        self.solution = {}
        self.orders = {}

        for gene in self.genes:
            gene.turn = None
            gene.penalty = 0
            self.__update_solution(gene)
            self.__update_orders(gene)

        self.__update_penalties()

        cumulative = 0
        for order_path in self.orders.values():
            cumulative += order_path.update_score()
        self.score = float(cumulative) / len(Problem.orders)

        return self.score - self.penalty

    def mutate(self):
        mutated_chromosome = deepcopy(self)

        mutation_prob = random.randint(0, 1)

        mutation_functions = [unbalance_quantities, switch_drones, join_genes]

        mutated_chromosome.genes = mutation_functions[random.randint(0, len(mutation_functions) - 1)](
            mutated_chromosome.genes)

        return mutated_chromosome

    def __update_solution(self, gene: Gene) -> None:
        if gene.droneID is None:
            return

        if not self.__path_exists(gene.droneID):
            self.__add_path(gene.droneID)

        path = self.__get_path(gene.droneID)
        last_step = path.get_last_step()
        if last_step is None:
            previous_position = Problem.warehouses[0].position
            previous_turns = 0
        else:
            previous_position = last_step.node.position
            previous_turns = last_step.turn

        gene.set_turns(previous_turns +
                       gene.node.position.distance(previous_position) +
                       1)
        path.add_step(gene)

    def __update_orders(self, gene: Gene):
        if isinstance(gene.node, Order):
            if not self.__order_exists(gene.node):
                self.__add_order(gene.node)

            order_path = self.__get_order(gene.node)
            order_path.add_step(gene)
        pass

    def __update_penalties(self):
        for drone_path in self.solution.values():
            self.penalty += check_payload(drone_path, Problem.products, Problem.payload)
            self.penalty += check_delivery(drone_path)

    def __path_exists(self, drone_id: int) -> bool:
        return True if drone_id in self.solution else False

    def __add_path(self, drone_id: int) -> None:
        self.solution[drone_id] = DronePath(drone_id)

    def __get_path(self, drone_id: int) -> DronePath:
        return self.solution.get(drone_id)

    def __order_exists(self, order: Order) -> bool:
        return True if order.id in self.orders else False

    def __add_order(self, order: Order) -> None:
        self.orders[order.id] = OrderPath(order)

    def __get_order(self, order: Order) -> OrderPath:
        return self.orders[order.id]

    def __eq__(self, o: Chromosome) -> bool:
        if len(self.genes) != len(o.genes): return False
        for i in range(0, len(self.genes)):
            if self.genes[i] != o.genes[i]: return False
        return True


class Shipment:
    def __init__(self, drone_path: DronePath, order: Order, warehouse: Warehouse):
        self.drone_path = drone_path
        self.order = order
        self.warehouse = warehouse
        self.products: dict[Product, int] = {}
        self.product_weight = 0
        self.turns = 0
        self.score = 0
        self.accomplishment = 0
        self.wh_distance = 0
        self.ord_distance = 0

        self.create()

    def create(self):
        prods: list[tuple[Product, int]] = []
        for product, quantity in self.order.products.items():
            available = min(quantity, self.warehouse.products.get(product, 0))
            if available > 0:
                prods.append((product, available))

        prods = sorted(prods, key=lambda p: -p[0].weight)
        drone_payload = Problem.payload
        carrying: dict[Product, int] = {}

        for product, quantity in prods:
            while quantity > 0:
                if product.weight <= drone_payload:
                    drone_payload -= product.weight
                    if product in carrying.keys():
                        carrying[product] += 1
                    else:
                        carrying[product] = 1
                    quantity -= 1
                else:
                    break

        self.products = carrying
        self.product_weight = sum(p.weight * q for p, q in self.products.items())
        self.accomplishment = self.product_weight / self.order.product_weight

        self.calculate_score()

    def calculate_score(self):
        self.wh_distance = self.drone_path.current_position.distance(self.warehouse.position)
        self.ord_distance = self.warehouse.position.distance(self.order.position)
        self.turns = self.wh_distance + self.ord_distance + len(self.products) * 2
        self.score = self.accomplishment / self.turns

    def has_products(self):
        return len(self.products) > 0

    def execute(self, chromosome):
        self.warehouse.remove_products(self.products)
        self.order.remove_products(self.products)
        self.drone_path.set_position(self.order.position)
        self.drone_path.add_shipment(self)

        # update chromosome load genes
        for product, quantity in self.products.items():
            chromosome.add_gene(
                Gene(self.drone_path.drone_id, quantity, self.warehouse, product, self.drone_path.turns + 1))

        self.drone_path.add_turns(self.turns)

        # update chromosome unload genes
        for product, quantity in self.products.items():
            chromosome.add_gene(
                Gene(self.drone_path.drone_id, -quantity, self.order, product, self.drone_path.turns + 1))

        return int(self.order.complete())
