def check_turns(drone_path, turns):
    """
    The max turns on a gene must not be higher than the max allowed turns

    :param drone_path: list containing the paths for every drone
    :param turns: max turns allowed
    :return: 0 if the constraint was fulfilled, 0 otherwise
    """
    final_turn = max(gene.turn for gene in drone_path.steps)
    if final_turn > turns:
        return 1
    return 0


def check_payload(drone_path, products, prob_payload):
    """
    Checks if any drone exceeded the max allowed payload

    :param drone_path: list containing the paths for every drone
    :param products: list containing the problem's products
    :param prob_payload: max payload allowed for a drone
    :return: the number of times this constraint was unfulfilled
    """

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
    """
    Checks if the drones have the product and the necessary amount before every delivery

    :param drone_path:  list containing the paths for every drone
    :return: the number of times this constraint was unfulfilled
    """

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
