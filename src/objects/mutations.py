from copy import deepcopy

from numpy import random
import objects.primitives as prim


def switch_drones(genes: list) -> list:
    """
    Switches the drones of 2 genes (works with None drone_id's)
    :param genes: List of genes to be altered
    :return: Altered list of genes
    """
    gene1_ind = random.randint(0, len(genes))
    drone1 = genes[gene1_ind].drone_id

    dif_drones: list[(int, prim.Gene)] = list(filter(lambda x: x[1].drone_id != drone1, enumerate(genes)))

    if not dif_drones:
        return genes

    gene2_ind, gene2 = dif_drones[random.randint(0, len(dif_drones))] if len(dif_drones) > 1 else dif_drones[0]
    drone2 = gene2.drone_id

    genes[gene1_ind].set_drone(drone2)
    genes[gene2_ind].set_drone(drone1)

    return genes


def unbalance_quantities(genes: list) -> list:
    """
    Unbalances the quantities of 2 genes of the same WareHouse and Product
    :param genes: List of genes to be altered
    :return: Altered list of genes
    """
    supplies = {}
    for i, gene in enumerate(genes):
        if gene.demand < 0: continue
        if (gene.node, gene.product) not in supplies:
            supplies[(gene.node, gene.product)] = [(i, gene)]
        else:
            supplies[(gene.node, gene.product)].append((i, gene))

    supplies_filter = {k: v for (k, v) in supplies.items() if len(v) > 1}

    if not supplies_filter:  # there aren't any 2 genes with same WH and item
        return genes

    index = random.randint(0, len(supplies_filter))
    supply_genes = supplies_filter[list(supplies_filter.keys())[index]]

    g1_pos = random.randint(0, len(supply_genes))
    values = list(range(0, len(supply_genes)))
    values.remove(g1_pos)
    g2_pos = random.choice(values)

    g1 = genes[supply_genes[g1_pos][0]]
    g2 = genes[supply_genes[g2_pos][0]]

    demand = g1.demand + g2.demand
    g1.demand = random.randint(1, demand)
    g2.demand = demand - g1.demand

    return genes


def cleanse_genes(genes: list) -> list:
    """
    Removes genes with penalties higher than 0
    :param genes: List of genes to be altered
    :return: Altered list of genes
    """
    return list(filter(lambda x: x.penalty == 0, genes))


def pop_gene(genes: list) -> list:
    """
    Removes the gene with the highest penalty
    :param genes: List of genes to be altered
    :return: Altered list of genes
    """
    sorted_genes = sorted(genes, key=lambda x: -x.penalty)
    genes.remove(sorted_genes[0])
    return genes


def join_genes(genes: list) -> list:
    """
    Merges 2 genes of the same Spot and Product, adding the quantities and choosing one of the two drone_id's
    :param genes: List of genes to be altered
    :return: Altered list of genes
    """
    gene_dic = {}

    for i, gene in enumerate(genes):
        if (gene.node, gene.product) not in gene_dic:
            gene_dic[(gene.node, gene.product)] = [(i, gene)]
        else:
            gene_dic[(gene.node, gene.product)].append((i, gene))

    gene_filter = {k: v for (k, v) in gene_dic.items() if len(v) > 1}

    if not gene_filter:  # there aren't any 2 genes with same WH and item
        return genes

    index = random.randint(0, len(gene_filter))
    sample_genes = gene_filter[list(gene_filter.keys())[index]]

    g1_pos = random.randint(0, len(sample_genes))
    values = list(range(0, len(sample_genes)))
    values.remove(g1_pos)
    g2_pos = random.choice(values)

    g1: prim.Gene = genes[sample_genes[g1_pos][0]]
    g2: prim.Gene = genes[sample_genes[g2_pos][0]]

    drone_id = g1.drone_id if random.randint(0, 2) else g2.drone_id
    demand = g1.demand + g2.demand
    node = g1.node
    product = g1.product
    new_gene = prim.Gene(drone_id, demand, node, product)

    new_gene_pos = g1_pos if random.randint(0, 2) else g2_pos
    genes.insert(new_gene_pos, new_gene)
    genes.remove(g1)
    genes.remove(g2)

    return genes


def add_gene(genes: list):
    """
    Adds a Gene of a product available in one of the warehouses
    :param genes: List of genes to be altered
    :return: Altered list of genes
    """
    # copy WH
    warehouses = deepcopy(prim.Problem.warehouses)

    # remover produtos que estão nos genes[]
    for gene in genes:
        gene_quantity = gene.demand
        if gene_quantity < 0:    # not a WH
            continue
        product_id = gene.product.id
        wh = next((wh for wh in warehouses if wh.id == gene.node.id), None)
        assert wh

        wh_quantity = wh.products.get(product_id)

        if wh_quantity is None:
            continue

        wh.remove_products({product_id: gene_quantity})

        if wh.complete():
            warehouses.remove(wh)

    # pegar num wh e um produto e uma quantidade, criar gene
    wh: prim.Warehouse = warehouses[random.randint(0, len(warehouses))]

    product_id = random.choice(list(wh.products.keys()))
    total = wh.products[product_id]

    if total <= 0:
        return genes
    amount = random.randint(1, total+1) if total > 0 else 1

    actual_wh = next((actual_wh for actual_wh in prim.Problem.warehouses if actual_wh.id == wh.id), None)
    assert actual_wh
    actual_product = next((actual_pd for actual_pd in prim.Problem.products if actual_pd.id == product_id), None)
    assert actual_product

    gene: prim.Gene = prim.Gene(None, amount, actual_wh, actual_product)

    genes.insert(random.randint(0, len(genes)), gene)

    return genes
