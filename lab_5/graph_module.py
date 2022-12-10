import random as rand
from itertools import combinations


def generate_rand_graph(n, p, min_d, max_d):
    nodes = list(range(1, n+1))
    adj_list = {i: [] for i in nodes}
    possible_edges = combinations(nodes, 2)
    for u, v in possible_edges:
        if rand.random() < p and len(adj_list[v]) < max_d and len(adj_list[u]) < max_d:
            adj_list[u].append(v)
            adj_list[v].append(u)
    for node, neighbours in adj_list.items():
        if len(neighbours) < min_d:
            nodes.remove(node)
            neighbours.append(rand.choice(nodes))
    return adj_list


def dump_graph():
    graph = generate_rand_graph(300, 0.90, 2, 30)
    with open("__graph_", "w") as f:
        f.write(str(graph))
    nodes_n = len(graph)
    return graph, nodes_n


def load_graph():
    with open("graph", "r") as f:
        graph = eval(f.read())
    nodes_n = len(graph)
    return graph, nodes_n


graph, nodes_n = dump_graph()
