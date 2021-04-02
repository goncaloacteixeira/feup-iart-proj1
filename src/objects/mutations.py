from numpy import random
from datetime import datetime
import objects.primitives as prim

# Trocar drones de 2 alelos para alterar trajetos (funciona com drones nulos)


def switch_drones(genes: list) -> list:
    random.seed(datetime.now().second.real)

    gene2, drone2 = 0, -1
    gene1 = random.randint(0, len(genes))
    drone1 = genes[gene1].droneID

    while drone1 == drone2:
        gene2 = random.randint(0, len(genes))
        drone2 = genes[gene2].droneID

    genes[gene1].set_drone(drone2)
    genes[gene2].set_drone(drone1)

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


# Junta 2 genes de deliver/supply num mesmo, com um dos drones, escolhido aleatório ficando na posição do 1º/2º
def join_genes(genes: list) -> list:
    gene_dic = {}

    for i, gene in enumerate(genes):
        if (gene.node, gene.product) not in gene_dic:
            gene_dic[(gene.node, gene.product)] = [(i, gene)]
        else:
            gene_dic[(gene.node, gene.product)].append((i, gene))

    gene_filter = {k: v for (k, v) in gene_dic.items() if len(v) > 1}
    index = random.randint(0, len(gene_filter))
    sample_genes = gene_filter[list(gene_filter.keys())[index]]

    g1_pos = random.randint(0, len(sample_genes))
    values = list(range(0, len(sample_genes)))
    values.remove(g1_pos)
    g2_pos = random.choice(values)

    g1: prim.Gene = genes[sample_genes[g1_pos][0]]
    g2: prim.Gene = genes[sample_genes[g2_pos][0]]

    drone_id = g1.droneID if random.randint(0, 2) else g2.droneID
    demand = g1.demand + g2.demand
    node = g1.node
    product = g1.product
    new_gene = prim.Gene(drone_id, demand, node, product)

    new_gene_pos = g1_pos if random.randint(0, 2) else g2_pos
    genes.insert(new_gene_pos, new_gene)
    genes.remove(g1)
    genes.remove(g2)

    return genes
