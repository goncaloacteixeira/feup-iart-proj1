from abc import ABC, abstractmethod


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "[POINT] X={x} Y={y}".format(x=self.x, y=self.y)


class Product:
    def __init__(self, id: int, weight: int):
        self.id = id
        self.weight = weight

    def __str__(self) -> str:
        return "[PRODUCT {id}] - weight={weight}".format(id=self.id, weight=self.weight)


class Warehouse:
    def __init__(self, id: int, position: Point, products: dict):
        self.id = id
        self.position = position
        self.products = products

    def __str__(self) -> str:
        products = ""
        for product in self.products:
            products += str(product) + "\n"

        return "[WAREHOUSE {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)


class Order:
    def __init__(self, id: int, position: Point, products: dict):
        self.id = id
        self.position = position
        self.products = products

    def __str__(self) -> str:
        products = ""
        for product in self.products:
            products += str(product) + "\n"

        return "[ORDER {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)


class Command(ABC):
    @abstractmethod
    def type(self):
        pass


class LoadCommand(Command):
    def type(self):
        print("Load")


class DeliverCommand(Command):
    def type(self):
        print("Deliver")