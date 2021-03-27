import math
from abc import ABC, abstractmethod
from typing import Union


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "[POINT] X={x} Y={y}".format(x=self.x, y=self.y)

    def distance(self, point) -> int:
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
    def __init__(self, rows: int, cols: int, drones: int, turns: int, payload: int, warehouses: list[Warehouse],
                 orders: list[Order]):
        self.rows = rows
        self.cols = cols
        self.drones = drones
        self.turns = turns
        self.payload = payload
        self.warehouses = warehouses
        self.orders = orders


class Gene:
    def __init__(self, drone_id: Union[int, None], demand: int, node: Spot, product: Product, turn: int = None):
        self.droneID = drone_id
        self.demand = demand
        self.node = node
        self.product = product
        self.turn = turn

    def __str__(self) -> str:
        return "[ {droneID} | {demand} | {node} | {productID} | {turns} ]".format(droneID=self.droneID,
                                                                                  demand=self.demand,
                                                                                  node=self.node.id,
                                                                                  productID=self.product.id,
                                                                                  turns=self.turn)

    def set_drone(self, drone) -> None:
        self.droneID = drone

    def set_turns(self, turns) -> None:
        self.turn = turns


class DronePath:
    def __init__(self, drone_id: int, steps: list[Gene] = None):
        if steps is None:
            steps = []
        self.drone_id = drone_id
        self.steps = steps

    def __str__(self):
        print("DRONE ", self.drone_id)
        [print(str(x)) for x in self.steps]
        return ""

    def get_last_step(self) -> Union[Gene, None]:
        try:
            return self.steps[-1]
        except IndexError:  # if steps = []
            return None

    def add_step(self, gene: Gene):
        self.steps.append(gene)


class Chromosome:
    def __init__(self, genes, solution: list[DronePath] = None):
        self.genes = genes
        self.solution = solution

    def __str__(self) -> str:
        genes = ""
        for gene in self.genes:
            genes += str(gene) + "\n"
        return genes

    def add_gene(self, gene):
        self.genes.append(gene)
