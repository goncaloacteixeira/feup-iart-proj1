def export_data(drone_paths, filename) -> list[str]:
    """
    Exports the Chromossome to a file
    :param drone_paths: DronePaths to get the info of the path of each drone
    :param filename: Resulting file name
    :return: List of the created commands
    """
    f = open(filename, 'w')

    paths = [x for x in drone_paths.values()]

    commands = ["{drone_id} {type} {node} {product} {number}"
                    .format(drone_id=step.drone_id, type="L" if step.demand > 0 else "D", node=step.node.id,
                            product=step.product.id, number=abs(step.demand))
                for path in paths for step in path.steps]

    commands.insert(0, str(len(commands)))

    f.write("\n".join(commands))
    f.close()
    return commands
