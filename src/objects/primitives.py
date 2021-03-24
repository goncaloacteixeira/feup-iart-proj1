import enum
import math
from abc import ABC, abstractmethod


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
    def __init__(self, droneID: int, demand: int, node: Spot, productID: int):
        self.droneID = droneID
        self.demand = demand
        self.node = node
        self.productID = productID

    def __str__(self) -> str:
        return "[ {droneID} | {demand} | {node} | {productID} ]".format(droneID=self.droneID, demand=self.demand,
                                                                        node=self.node.id, productID=self.productID)

    def set_drone(self, drone) -> None:
        self.droneID = drone


class Chromosome:
    def __init__(self, genes):
        self.genes = genes

    def __str__(self) -> str:
        genes = ""
        for gene in self.genes:
            genes += str(gene) + "\n"
        return genes

    def add_gene(self, gene):
        self.genes.append(gene)


class DroneAction(enum.Enum):
    P = 1  # PickUp
    D = 2  # Deliver
