from Tree import *


def flatten(nested):
    return [item for sublist in nested for item in sublist]


def contains_goal(nodes: list, number):
    solutions = []
    for node in nodes:
        if node.supplies == number:
            solutions.append(node.info)
    return solutions


def is_goal(node, number):
    return node.supplies == number


def find_path(node: Node):
    path = [node]

    while node.parent is not None:
        path.append(node.parent)
        node = node.parent

    path.reverse()
    return path


def print_path(path: list):
    for node in path:
        print(node.info)
