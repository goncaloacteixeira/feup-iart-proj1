
def check_turns(chromosome, problem):
    for droneID in range(problem.drones-1):
        turns = 0
        last_gene = None
        for gene in chromosome.genes:
            if gene.droneID == droneID:
                if last_gene is not None:
                    turns += last_gene.node.position.distance(gene.node.position) + 1
                last_gene = gene
        if turns > problem.turns:
            return False
    return True


def check_payload(chromosome, problem):
    for droneID in range(problem.drones-1):
        payload = 0
        for gene in chromosome.genes:
            if gene.droneID == droneID:
                if gene.demand > 0:
                    payload += gene.demand*problem.products[gene.productID].weight
                else:
                    if payload > problem.payload:
                        return False
                    payload = 0
    return True


#def check_pick_up(chromosome, problem):
#    wh_copy = problem.warehouses.copy()
#    for warehouse in wh_copy:
#        for gene in chromosome.genes:
#            if gene.node.position == warehouse.position:
#                warehouse.products[problem.products[gene.productID]] = warehouse.products[problem.products[gene.productID]] + gene.demand
#                if gene.demand > 0 and warehouse.products[problem.products[gene.productID]] < 0:  # drone picked up a product quantity that was not available
#                    return False
#    return True



