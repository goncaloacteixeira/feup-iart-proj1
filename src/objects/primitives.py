from __future__ import annotations
import math
from abc import ABC, abstractmethod
from typing import Union

from src.constraints import *


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

    def __str__(self) -> str:
        products = ""
        for product, quantity in self.products.items():
            products += str(product) + " quantity=" + str(quantity) + "\n"
        return "[ORDER {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)


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


class Gene:
    def __init__(self, drone_id: Union[int, None], demand: int, node: Spot, product: Product, turn: int = None):
        self.droneID = drone_id
        self.demand = demand
        self.node = node
        self.product = product
        self.turn = turn
        self.penalty = 0

    def __str__(self) -> str:
        return "[ {droneID} | {demand} | {node} | {productID} | {turns} | {penalty} ]".format(droneID=self.droneID,
                                                                                              demand=self.demand,
                                                                                              node=self.node.id,
                                                                                              productID=self.product.id,
                                                                                              turns=self.turn,
                                                                                              penalty=self.penalty)

    def set_drone(self, drone: int) -> None:
        self.droneID = drone

    def set_turns(self, turns: int) -> None:
        self.turn = turns


class DronePath:
    def __init__(self, drone_id: int, steps: list[Gene] = None):
        if steps is None:
            steps = []
        self.drone_id = drone_id
        self.steps = steps

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
        # TODO Cada gene terá penalização, subtrai-se no final
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

    def __str__(self) -> str:
        genes = ""
        for gene in self.genes:
            genes += str(gene) + "\n"
        return genes

    def add_gene(self, gene: Gene) -> None:
        self.genes.append(gene)

    def print_solution(self):
        for key, value in self.solution.items():
            print(value)

    def print_orders(self):
        for key, value in self.orders.items():
            print(value)

    def update_internal(self):
        """ Updates Solution, orders and value of this chromosome """
        for gene in self.genes:
            self.__update_solution(gene)
            self.__update_orders(gene)

        self.__update_penalties()

        cumulative = 0
        for order_path in self.orders.values():
            cumulative += order_path.update_score()
        self.score = float(cumulative) / len(Problem.orders)

    def __update_solution(self, gene: Gene):
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
        pass

    def __update_orders(self, gene: Gene):
        if isinstance(gene.node, Order):
            if not self.__order_exists(gene.node):
                self.__add_order(gene.node)

            order_path = self.__get_order(gene.node)
            order_path.add_step(gene)
        pass

    def __update_penalties(self):
        for drone_path in self.solution.values():
            check_payload(drone_path, Problem.products, Problem.payload)
            check_delivery(drone_path)

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
