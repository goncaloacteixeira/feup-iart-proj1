from __future__ import annotations
import math
from abc import ABC, abstractmethod
from typing import Union
from collections import Counter

from objects.mutations import *
from search.constraints import *


class Point:
    def __init__(self, x: int, y: int):
        """
        Object that represents a point in the map
        :param x: The position of the column
        :param y: The position of the row
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """
        The String representation of a Point
        :return: [POINT] X={x} Y={y}
        """
        return "[POINT] X={x} Y={y}".format(x=self.x, y=self.y)

    def distance(self, point: 'Point') -> int:
        """
        Distance calculated between 2 points
        :param point: Another point to calculate distance
        :return: The calculated distance
        """
        return math.ceil(math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2))


class Product:
    def __init__(self, id: int, weight: int):
        """
        Product object with and identifier and weight
        :param id: identifier of the product
        :param weight: weight of the product
        """
        self.id = id
        self.weight = weight

    def __str__(self) -> str:
        """
        String representation of the Product object
        :return: [PRODUCT {id}] - weight={weight}
        """
        return "[PRODUCT {id}] - weight={weight}".format(id=self.id, weight=self.weight)


class Spot(ABC):
    @abstractmethod
    def __init__(self, id: int, position: Point, products: dict[int, int]):
        """
        Object representing a place in the map
        :param id: identifier of the Spot
        :param position: Position of the Spot
        :param products: Products and quantities associated with that spot
        """
        self.id = id
        self.position = position
        self.products = products

    def add_products(self, products: dict[int, int]) -> None:
        """
        Adds the products from the arguments to this spot
        :param products: list of products and quantities to add
        """
        for product, quantity in products.items():
            if product in self.products:
                self.products[product] += quantity
            else:
                self.products[product] = quantity

    def remove_products(self, products: dict[int, int]) -> None:
        """
        Removes the products from the list from this spot
        :param products: list of products to be removed
        """
        for product, quantity in products.items():
            self.products[product] -= quantity
            if self.products[product] == 0:
                self.products.pop(product)

    def complete(self) -> bool:
        """
        Check if the list of products is empty
        :return: true if the list is empty
        """
        return not self.products


class Warehouse(Spot):
    def __init__(self, id: int, position: Point, products: dict[int, int]):
        """
        An instance of Spot. A warehouse that holds products
        :param id: identifier of the warehouse
        :param position: Position in the map
        :param products: List of products in the warehouse
        """
        super().__init__(id, position, products)

    def __str__(self) -> str:
        """
        String representation of a WareHouse, including products
        :return: [WAREHOUSE {id}] - position={position} | {products}
        """
        products = ""
        for product, amount in self.products.items():
            products += str(product) + " amount=" + str(amount) + "\n"
        return "[WAREHOUSE {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)

    def has_any_product(self, products: dict) -> bool:
        """
        Checks if the Warehouse has any of the products in the dict
        :param products: list of products
        :return: true if the warehouse has any of the products
        """
        for k, v in products.items():
            if self.products.get(k, -1) > 0:
                return True
        return False


class Order(Spot):
    def __init__(self, id: int, position: Point, products: dict[int, int]):
        """
        Instance of Spot corresponding to a Order
        :param id: identifier of the order
        :param position: Position of the Order
        :param products: List of produts to be deliveres
        """
        super().__init__(id, position, products)
        self.product_weight = 0

    def __str__(self) -> str:
        """
        String representation of an Order
        :return: [ORDER {id}] - position={position} | {products}
        """
        products = ""
        for product, quantity in self.products.items():
            products += str(product) + " quantity=" + str(quantity) + "\n"
        return "[ORDER {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)

    def update_weight(self) -> None:
        """
        updates the order weight based on the product list
        """
        self.product_weight = sum(Problem.get_product(p).weight * q for p, q in self.products.items())


class Problem:
    rows: int = None
    cols: int = None
    drones: int = None
    turns: int = None
    payload: int = None
    warehouses: list[Warehouse] = None
    orders: list[Order] = None
    products: list[Product] = None

    @staticmethod
    def get_product(product_id: int) -> Product:
        """
        Retrieve a Product by its id
        :param product_id: identifier of the product
        :return: Product retrieved
        """
        return Problem.products[product_id]

    @staticmethod
    def calculate_points(turn: int) -> int:
        """
        Calculates the points given the turns
        :param turn: turns
        :return: score
        """
        return math.ceil(((Problem.turns - turn) / Problem.turns) * 100)

    @staticmethod
    def read_file(file_path: str) -> None:
        """
        Reads a file and fills the Problems values
        :param file_path: path to the .in file
        """
        [Problem.rows, Problem.cols, Problem.drones, Problem.turns, Problem.payload, Problem.warehouses, Problem.orders,
         Problem.products] = Problem.parse_file(file_path)
        for order in Problem.orders:
            order.update_weight()

    @staticmethod
    def parse_file(filename: str) -> tuple[int, int, int, int, int, list[Warehouse], list[Order], list[Product]]:
        """Parsing of the .in file

        :param filename: path to the .in file
        :return: data
        """
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
                warehouse_products = {product.id: n for product, n in zip(products, n_products_warehouse)}
                warehouse = Warehouse(i, Point(x, y), warehouse_products)
                warehouses.append(warehouse)

            # order
            order_list = []
            n_orders = int(file.readline())
            for i in range(n_orders):
                x, y = map(int, file.readline().split(" "))
                n_products_in_order = int(file.readline())
                order_products = list(map(int, file.readline().split(" ")))  # applies int() to each element
                # to ensure the number of products in order actually corresponds to the number of products listed
                assert n_products_in_order == len(order_products)
                # order_products = [products[x] for x in order_products]      # list[int] -> list[Product]
                order = Order(i, Point(x, y), dict(Counter(order_products)))
                order_list.append(order)

        return n_rows, n_cols, n_drones, max_turns, max_payload, warehouses, order_list, products


class Gene:
    def __init__(self, drone_id: Union[int, None], demand: int, node: Spot, product: Product, turn: int = None):
        """
        Gene Constructor. Part of the Solution
        :param drone_id: identifier of the drone
        :param demand: quantity of product
        :param node: Warehouse or Order
        :param product: Product object
        :param turn: turn of execution. Defaults to None.
        """
        self.drone_id = drone_id
        self.demand = demand
        self.node = node
        self.product = product
        self.turn = turn
        self.penalty = 0

    def __str__(self) -> str:
        """
        String representation of Gene
        :return: [ {droneID} | {demand} | {productID} | {node} | {turns} | {penalty} ]
        """
        return "[ {droneID} | {demand} | {productID} | {node} | {turns} | {penalty} ]".format(droneID=self.drone_id,
                                                                                              demand=self.demand,
                                                                                              node=self.node.id,
                                                                                              productID=self.product.id,
                                                                                              turns=self.turn,
                                                                                              penalty=self.penalty)

    def set_drone(self, drone: int) -> None:
        """
        Sets the drone_id
        :param drone: drone_id
        """
        self.drone_id = drone

    def set_turns(self, turns: int) -> None:
        """
        Sets the Gene turns
        :param turns: turns
        """
        self.turn = turns

    def __eq__(self, o: Gene) -> bool:
        """
        Checks if 2 Genes are equals
        :param o: The other Gene to compare
        :return: true if the Genes are equal
        """
        return self.drone_id == o.drone_id and self.demand == o.demand and self.node.id == o.node.id and self.product.id == o.product.id and self.turn == o.turn

    def __hash__(self) -> int:
        return super().__hash__()


class DronePath:
    def __init__(self, drone_id: int, current_position: Point = Point(0, 0), steps: list[Gene] = None):
        """
        Drone Path constructor
        :param drone_id: Drone identifier
        :param current_position: Current position of the Drone. Defaults to Point(0, 0).
        :param steps: list of Genes of that Drone. Defaults to None.
        """
        if steps is None:
            steps = []
        self.drone_id = drone_id
        self.steps = steps
        self.shipments = []
        self.current_position = current_position
        self.turns = 0

    def __str__(self) -> str:
        """
        String representation of the DronePath
        :return: DRONE and list
        """
        print("DRONE ", self.drone_id)
        [print(str(gene)) for gene in self.steps]
        return ""

    def get_last_step(self) -> Union[Gene, None]:
        """
        Gets last step of the gene list
        :return: Returns None id list is empty or last step
        """
        try:
            return self.steps[-1]
        except IndexError:  # if steps = []
            return None

    def add_step(self, gene: Gene) -> None:
        """
        Adds a gene to the list of genes
        :param gene: Gene to append
        :return:
        """
        self.steps.append(gene)

    def set_position(self, position: Point) -> None:
        """
        Sets the current position of the drone
        :param position: Position
        """
        self.current_position = position

    def add_shipment(self, shipment: Shipment) -> None:
        """
        Adds a shipment to the Drone Path
        :param shipment: Shipment to append
        """
        self.shipments.append(shipment)

    def add_turns(self, turns: int) -> None:
        """
        adds turns to the DronePaht
        :param turns: amount of turns to add
        """
        self.turns += turns


class OrderPath:
    def __init__(self, order: Order, steps: list[Gene] = None, score: int = 0):
        """
        Path of the Order
        :param order: Order object associated to this path
        :param steps: List of Genes of this Order
        :param score: Score of this order
        """
        if steps is None:
            steps = []
        self.order = order
        self.steps = steps
        self.score = score  # calculated score for this order

    def __str__(self) -> str:
        """
        String representation of the OrderPath
        :return: "ORDER " + list
        """
        print("ORDER ", self.order.id)
        [print(str(gene)) for gene in self.steps]
        return ""

    def add_step(self, gene: Gene) -> None:
        """
        Appends a Gene to the list of steps
        :param gene: gene to append
        :return: None
        """
        self.steps.append(gene)

    def update_score(self) -> int:
        """
        Updates the Drone Path score
        :return: Updated Score
        """
        maximum = max(gene.turn for gene in self.steps)
        self.score = Problem.calculate_points(maximum)
        return self.score


class Chromosome:
    def __init__(self, genes: list[Gene] = None, solution: dict[int, DronePath] = None,
                 orders: dict[int, OrderPath] = None, score: int = 0):
        """
        The representation of the solution
        :param genes: List of genes
        :param solution: dictionary of DronePaths for each Drone
        :param orders: dictionary of OrderPaths for each Order
        :param score: Score of the solution
        """
        if orders is None: orders = {}
        if genes is None: genes = []
        if solution is None: solution = {}
        self.genes = genes
        self.solution = solution
        self.orders = orders
        self.score = score
        self.penalty = 0

    def __str__(self) -> str:
        """
        String representation of the chromosome
        :return: Representation of each Gene
        """
        return "\n".join([str(gene) for gene in self.genes])

    def __repr__(self) -> str:
        """
        Compact representation of the chromosome
        :return: [Chromosome] Genes: {genes} | Penalty: {penalty} | Score: {score}
        """
        return "[Chromosome] Genes: {genes} | Penalty: {penalty} | Score: {score}".format(genes=len(self.genes),
                                                                                          penalty=self.penalty,
                                                                                          score=self.score)

    def add_gene(self, gene: Gene) -> None:
        """
        Appends a Gene to the gene list
        :param gene: Gene to be appended
        :return: None
        """
        self.genes.append(gene)

    def print_solution(self) -> None:
        """
        Prints each DronePath of the solution
        """
        for key, value in self.solution.items():
            print(value)

    def print_orders(self) -> None:
        """
        Prints each OrderPath of the solution
        """
        for key, value in self.orders.items():
            print(value)

    def update_internal(self) -> float:
        """
        Updates Solution, orders and value of this chromosome
        :return: The score with the penalties subtracted
        """
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

    def mutate(self) -> Chromosome:
        """
        Applies a mutation to the current chromosome
        :return: the new mutated chromosome
        """
        mutated_chromosome = deepcopy(self)

        mutation_functions = [unbalance_quantities, join_genes, pop_gene, cleanse_genes, switch_drones, add_gene]

        mutated_chromosome.genes = mutation_functions[random.randint(0, len(mutation_functions))](
            mutated_chromosome.genes)

        return mutated_chromosome

    def clean(self) -> Chromosome:
        """
        Removes the genes with drone_id None from the chromosome
        :return: the cleaned chromosome
        """
        self.genes = list(filter(lambda x: x.drone_id is not None, self.genes))
        return self

    def __update_solution(self, gene: Gene) -> None:
        """
        Updates the internal values of the chromosome DronePaths
        :param gene: Gene to be evaluated
        """
        if gene.drone_id is None:
            return

        if not self.__path_exists(gene.drone_id):
            self.__add_path(gene.drone_id)

        path = self.__get_path(gene.drone_id)
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

    def __update_orders(self, gene: Gene) -> None:
        """
        Updates the internal values of the chromosome OrderPaths
        :param gene: Gene to be evaluated
        """
        if gene.drone_id is None:
            return
        if isinstance(gene.node, Order):
            if not self.__order_exists(gene.node):
                self.__add_order(gene.node)

            order_path = self.__get_order(gene.node)
            order_path.add_step(gene)
        pass

    def __update_penalties(self) -> None:
        """
        Updates the penalties of each DronePath
        """
        for drone_path in self.solution.values():
            self.penalty += check_payload(drone_path, Problem.products, Problem.payload)
            self.penalty += check_delivery(drone_path)
            self.penalty += check_turns(drone_path, Problem.turns)

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
        """
        Checks if 2 Chromossomes are equal
        :param o: The other Chromossome to be evaluated
        :return: true if the chromossomes are the same
        """
        if len(self.genes) != len(o.genes): return False
        for i in range(0, len(self.genes)):
            if self.genes[i] != o.genes[i]: return False
        return True


class Shipment:
    def __init__(self, drone_path: DronePath, order: Order, warehouse: Warehouse):
        """
        Shipment representing a trip to a warehouse and a trip to the order Point
        :param drone_path: DronePath to associate the Shipment to a Drone
        :param order: Order that will received products
        :param warehouse: WareHouse from where the products will be taken
        """
        self.drone_path = drone_path
        self.order = order
        self.warehouse = warehouse
        self.products: dict[int, int] = {}
        self.product_weight = 0
        self.turns = 0
        self.score = 0
        self.accomplishment = 0
        self.wh_distance = 0
        self.ord_distance = 0

        self.create()

    def create(self) -> None:
        """
        Creates a Shipment and checks which products the drone can carry
        """
        prods: list[tuple[int, int]] = []
        for product_id, quantity in self.order.products.items():
            available = min(quantity, self.warehouse.products.get(product_id, 0))
            if available > 0:
                prods.append((product_id, available))

        prods = sorted(prods, key=lambda p: -Problem.get_product(p[0]).weight)
        drone_payload = Problem.payload
        carrying: dict[int, int] = {}

        for product_id, quantity in prods:
            while quantity > 0:
                if Problem.get_product(product_id).weight <= drone_payload:
                    drone_payload -= Problem.get_product(product_id).weight
                    if product_id in carrying.keys():
                        carrying[product_id] += 1
                    else:
                        carrying[product_id] = 1
                    quantity -= 1
                else:
                    break

        self.products = carrying
        self.product_weight = sum(Problem.get_product(p).weight * q for p, q in self.products.items())
        self.accomplishment = self.product_weight / self.order.product_weight

        self.calculate_score()

    def calculate_score(self) -> None:
        """
        Calculates the Shipment Score
        """
        self.wh_distance = self.drone_path.current_position.distance(self.warehouse.position)
        self.ord_distance = self.warehouse.position.distance(self.order.position)
        self.turns = self.wh_distance + self.ord_distance + len(self.products) * 2
        self.score = self.accomplishment / self.turns

    def has_products(self) -> int:
        """
        Checks if the Shipment has Products
        :return: Numbers of products in the shipment
        """
        return len(self.products) > 0

    def execute(self, chromosome: Chromosome) -> int:
        """
        Executes the Shipment, removing the products from the WareHouse and Orders, and updating the Drone
        :param chromosome: Chromossome to add Genes to
        :return: Number of orders completed
        """
        self.warehouse.remove_products(self.products)
        self.order.remove_products(self.products)
        self.drone_path.set_position(self.order.position)
        self.drone_path.add_shipment(self)

        # update chromosome load genes
        for product_id, quantity in self.products.items():
            chromosome.add_gene(
                Gene(self.drone_path.drone_id, quantity, self.warehouse, Problem.get_product(product_id),
                     self.drone_path.turns + 1))

        self.drone_path.add_turns(self.turns)

        # update chromosome unload genes
        for product_id, quantity in self.products.items():
            chromosome.add_gene(
                Gene(self.drone_path.drone_id, -quantity, self.order, Problem.get_product(product_id),
                     self.drone_path.turns))

        return int(self.order.complete())
