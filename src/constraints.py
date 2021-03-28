
def check_turns(drone_path, problem):
    final_turn = max(gene.turn for gene in drone_path.genes)
    if final_turn > problem.turns:
        return False
    return True


def check_payload(drone_path, problem):
    #TODO check logo depois de adicionar a payload
    payload = 0
    for gene in drone_path.genes:
        if gene.demand > 0:
            payload += gene.demand*problem.products[gene.productID].weight
        else:
            if payload > problem.payload:
                return False
            payload = 0
    return True


def check_delivery(drone_path):
    #TODO dict que mantem catálogo e nas entregas verifica se tem
    for gene in drone_path.genes:
        product_qt = 0
        if gene.demand < 0:
            for gene1 in drone_path.genes:  # checks previous genes
                if gene == gene1:
                    break
                elif gene1.productID == gene.productID:
                    product_qt += gene1.demand
            if product_qt + gene.demand < 0:
                return False
    return True
