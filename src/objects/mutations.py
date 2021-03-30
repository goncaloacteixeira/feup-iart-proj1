import random
from datetime import datetime
from copy import deepcopy


# Trocar drones de 2 alelos para alterar trajetos (funciona com drones nulos)
def switch_drones(genes: list) -> list:
    random.seed(datetime.now().second.real)

    drone1, drone2 = 0, 0
    gene1, gene2 = 0, 0
    while drone1 == drone2:
        gene1 = random.randint(0, len(genes) - 1)
        gene2 = random.randint(0, len(genes) - 1)
        drone1 = genes[gene1].droneID
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

    supply_genes = supplies[random.choice(list(supplies.keys()))]
    while len(supply_genes) < 2:
        supply_genes = supplies[random.choice(list(supplies.keys()))]

    g1_pos, g2_pos = 0, 0
    while g1_pos == g2_pos:
        g1_pos = random.randint(0, len(supply_genes) - 1)
        g2_pos = random.randint(0, len(supply_genes) - 1)

    g1 = genes[supply_genes[g1_pos][0]]
    g2 = genes[supply_genes[g2_pos][0]]

    demand = g1.demand + g2.demand
    g1.demand = random.randint(1, demand - 1)
    g2.demand = demand - g1.demand

    return genes


# Junta 2 genes de deliver/supply num mesmo, com um dos drones, escolhido aleatório ficando na posição do 1º/2º
def join_genes(genes: list) -> list:
    gene_dic = {}

    gene_type = random.randint(0, 1) # 0-deliver 1-supply

    for i, gene in enumerate(genes):
        if gene_type == 0 and gene.demand > 0: continue
        if gene_type == 1 and gene.demand < 0: continue

        if (gene.node, gene.product) not in gene_dic:
            gene_dic[(gene.node, gene.product)] = [(i, gene)]
        else:
            gene_dic[(gene.node, gene.product)].append((i, gene))

    sample_genes = gene_dic[random.choice(list(gene_dic.keys()))]
    if max(len(x) for x in sample_genes) < 2:
        return genes
    while len(sample_genes) < 2:
        sample_genes = gene_dic[random.choice(list(gene_dic.keys()))]

    g1_pos, g2_pos = 0, 0
    while g1_pos == g2_pos:
        g1_pos = random.randint(0, len(sample_genes) - 1)
        g2_pos = random.randint(0, len(sample_genes) - 1)

    g1 = genes[sample_genes[g1_pos][0]]
    g2 = genes[sample_genes[g2_pos][0]]
    demand = g1.demand + g2.demand
    new_gene = deepcopy(g1) if random.randint(0, 1) == 0 else deepcopy(g2)
    new_gene_pos = g1_pos if random.randint(0, 1) == 0 else g2_pos
    new_gene.demand = demand
    genes.insert(new_gene_pos, new_gene)
    genes.remove(g1)
    genes.remove(g2)

    return genes
