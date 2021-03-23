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
        for product, amount in self.products.items():
            products += str(product) + " amount=" + str(amount) + "\n"

        return "[WAREHOUSE {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)


class Order:
    def __init__(self, id: int, position: Point, products: dict):
        self.id = id
        self.position = position
        self.products = products

    def __str__(self) -> str:
        products = ""
        for product, quantity in self.products.items():
            products += str(product) + " quantity=" + str(quantity) + "\n"

        return "[ORDER {id}] - position={position}\n{products}" \
            .format(id=self.id, position=self.position, products=products)


class Gene:
    def __init__(self, droneID, demand, node, productID):
        self.droneID = droneID
        self.demand = demand
        self.node = node
        self.productID = productID

    def __str__(self) -> str:
        return "[ {droneID} | {demand} | {node} | {productID} ]".format(droneID=self.droneID, demand=self.demand,
                                                                        node=self.node, productID=self.productID)


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
