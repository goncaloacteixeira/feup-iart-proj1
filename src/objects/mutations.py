from copy import deepcopy

from numpy import random
import objects.primitives as prim


# Trocar drones de 2 alelos para alterar trajetos (funciona com drones nulos)
def switch_drones(genes: list) -> list:
    gene1_ind = random.randint(0, len(genes))
    drone1 = genes[gene1_ind].drone_id

    # lista de genes com drone != drone 1
    dif_drones: list[(int, prim.Gene)] = list(filter(lambda x: x[1].drone_id != drone1, enumerate(genes)))

    if not dif_drones:
        return genes

    # escolher um dessa lista
    gene2_ind, gene2 = dif_drones[random.randint(0, len(dif_drones))] if len(dif_drones) > 1 else dif_drones[0]
    drone2 = gene2.drone_id

    genes[gene1_ind].set_drone(drone2)
    genes[gene2_ind].set_drone(drone1)

    return genes


# 2 alelos do mesmo WH e item -> desiquilibrar as quantidades
def unbalance_quantities(genes: list) -> list:
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


# limpar genes com penalty diferente de 0
def cleanse_genes(genes: list) -> list:
    return list(filter(lambda x: x.penalty == 0, genes))


# remove o gene com maior penalty
def pop_gene(genes: list) -> list:
    sorted_genes = sorted(genes, key=lambda x: -x.penalty)
    genes.remove(sorted_genes[0])
    return genes


# Junta 2 genes de deliver/supply num mesmo, com um dos drones, escolhido aleatório ficando na posição do 1º/2º
def join_genes(genes: list) -> list:
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


# Adiciona um gene de um produto de um wh que não esteja
def add_gene(genes: list):
    # copy WH
    warehouses = deepcopy(prim.Problem.warehouses)

    # remover produtos que estão nos genes[]
    for gene in genes:
        product = gene.product
        quantity = gene.demand


    # escolher um produto e quantidade random
    # adicionar a genes[] com drone = None
    pass
