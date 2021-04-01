def check_turns(drone_path, turns):
    final_turn = max(gene.turn for gene in drone_path.steps)  # aplicar penalty aos genes todos ou só ao ultimo?
    if final_turn > turns:
        return 1
    return 0


def check_payload(drone_path, products, prob_payload):
    penalty = 1
    penalty_applied = 0

    payload = 0
    for gene in drone_path.steps:
        payload += gene.demand * products[gene.product.id].weight
        if payload > prob_payload:
            gene.penalty += penalty
            penalty_applied += penalty
    return penalty_applied


def check_delivery(drone_path):
    penalty = 1
    penalty_applied = 0

    products = {}
    for gene in drone_path.steps:
        if gene.demand > 0:
            if gene.product.id in products.keys():
                products[gene.product.id] += gene.demand
            else:
                products[gene.product.id] = gene.demand
        else:
            if gene.product.id not in products.keys() or abs(gene.demand) > products[gene.product.id]:
                gene.penalty += penalty
                penalty_applied += penalty
                continue
            products[gene.product.id] += gene.demand
    return penalty_applied
