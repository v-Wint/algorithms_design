from graph_module import graph
import random as rand


def add_rand_adj_node(c):
    nodes = []
    for i, gene in enumerate(c.chromosome):
        if gene:
            nodes.append(i + 1)

    rand.shuffle(nodes)
    for node in nodes:
        neighbours = graph[node]
        rand.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour in nodes:
                continue
            # if nodes in clique are all in neighbours of the neighbour of the node
            if set(nodes) <= set(graph[neighbour]):
                chromosome = list(c.chromosome)
                chromosome[neighbour-1] = 1
                c.update(chromosome)
                return


def add_adj_node_heuristic(c):
    nodes = []
    for i, gene in enumerate(c.chromosome):
        if gene:
            nodes.append(i + 1)

    rand.shuffle(nodes)
    neighbours = []
    for node in nodes:
        neighbours += graph[node]

    neighbours = list(set(neighbours))
    rand.shuffle(neighbours)

    for neighbour in sorted(neighbours, key=lambda x: len(graph[x])):
        if neighbour in nodes:
            continue
        # if nodes in clique are all in neighbours of the neighbour of the node
        if set(nodes) <= set(graph[neighbour]):
            chromosome = list(c.chromosome)
            chromosome[neighbour-1] = 1
            c.update(chromosome)
            return
