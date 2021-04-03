import math
import objects.primitives as prim


def deliverGenes(orders) -> list[prim.Gene]:
    list = []
    i = -1
    for order in orders:
        i += 1
        for product_id, quantity in order.products.items():
            product = prim.Problem.get_product(product_id)
            remaining = quantity
            max_product = math.floor(prim.Problem.payload / product.weight)  # max products per drone
            drones_needed = math.ceil(quantity / max_product)

            for i in range(drones_needed - 1):
                remaining -= max_product
                list.append(prim.Gene(None, -max_product, order, product))
            if remaining != 0:
                list.append(prim.Gene(None, -remaining, order, product))

    return list


def calculate_product(warehouse_available, needed) -> tuple[int, int]:
    if warehouse_available >= needed:
        available = warehouse_available - needed
        return available, 0
    else:
        still_need = needed - warehouse_available
        return 0, still_need


def naive_solution() -> prim.Chromosome:
    wh_copy = prim.Problem.warehouses.copy()
    chromosome = prim.Chromosome()
    drone = 0

    supplier_genes = deliverGenes(prim.Problem.orders)
    for gene in supplier_genes:
        remaining_product = abs(gene.demand)  # demand product
        for warehouse in wh_copy:
            if warehouse.products.get(gene.product.id) is not None:
                wh_quantity, needed = calculate_product(warehouse.products.get(gene.product.id), remaining_product)
                if wh_quantity < warehouse.products.get(gene.product.id):
                    chromosome.add_gene(
                        prim.Gene(drone, remaining_product - needed, warehouse, gene.product))  # add gene with pick up

                    warehouse.products.update({gene.product.id: wh_quantity})  # updates warehouse product
                    remaining_product = needed  # decrement demand product
                if remaining_product == 0:  # when demand is 0 we can add gene corresponding to delivery
                    gene.set_drone(drone)
                    chromosome.add_gene(gene)
                    drone += 1
                    if drone > prim.Problem.drones - 1:
                        drone = 0
                    break
    return chromosome
