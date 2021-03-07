from objects.primitives import *
from collections import Counter


def parse_file(filename):
    with open(filename, 'r') as file:
        # header
        n_rows, n_cols, n_drones, max_turns, max_payload = file.readline().split(" ")

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

    return n_rows, n_cols, n_drones, max_turns, max_payload, warehouses, order_list


if __name__ == "__main__":
    n_rows, n_cols, n_drones, max_turns, max_payload, warehouses, order_list = parse_file("input_data/demo.in")
    [print(order) for order in order_list]
