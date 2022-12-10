from random import shuffle
from queue import PriorityQueue
import networkx as nx

SCOUTS_N = 5
BEST_SCOUTS_N = 2
RANDOM_SCOUTS_N = SCOUTS_N - BEST_SCOUTS_N
FORAGERS_N = 55
BEST_FORAGERS_N = 20
RANDOM_FORAGERS_N = 5


class Bee:
    def __init__(self, coloring, f):
        self.coloring = coloring
        self.f = f

    def __lt__(self, other):
        return self.f.__lt__(other.f)

    def __repr__(self):
        return f"\nFunction: {self.f} Coloring: {self.coloring}"


def generate_rand_graph():
    g = nx.watts_strogatz_graph(300, 30, 1)
    graph = {}
    for edge in g.edges:
        u, v = edge
        u += 1
        v += 1
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)
    return graph


def in_neighbours(color, neighbours, coloring):
    if neighbours:
        for neighbour in neighbours:
            if neighbour in coloring and coloring[neighbour] == color:
                return True
    return False


def random_coloring(graph):
    coloring = {node: 0 for node in graph.keys()}
    graph = list(graph.items())
    shuffle(graph)
    max_color = 0
    for node, neighbours in graph:
        for color in range(1, 10000):
            if not in_neighbours(color, neighbours, coloring):
                coloring[node] = color
                if color > max_color:
                    max_color += 1
                break
    return coloring, max_color


def generate_scouts(graph, scouts, n):
    while scouts.qsize() < n:
        scout = Bee(*random_coloring(graph))
        if scout not in scouts.queue:
            scouts.put(scout)


def find_best_scouts(scouts):
    best = []
    for i in range(BEST_SCOUTS_N):
        best.append(scouts.get())
    return best


def discover(scout, graph, local_foragers_n):
    queue = []

    for node, neighbours in sorted(list(graph.items()), key=lambda x: len(x[1]), reverse=True):
        if len(queue) >= local_foragers_n:
            break
        for neighbour in neighbours:
            queue.append((node, neighbour))

    results = []

    for node, neighbour in queue:
        new_coloring = dict(scout.coloring)
        new_coloring[neighbour], new_coloring[node] = new_coloring[node], new_coloring[neighbour]

        if in_neighbours(new_coloring[node], graph[node], new_coloring) or \
                in_neighbours(new_coloring[neighbour], graph[neighbour], new_coloring):
            continue
        else:
            for color in range(1, scout.f + 1):
                if not in_neighbours(color, graph[neighbour], new_coloring):
                    new_coloring[neighbour] = color
                    results.append(Bee(new_coloring, len(set(new_coloring.values()))))

    return min(results, key=lambda x: x.f) if results else scout


def local_search(graph, new_scouts, scouts, n):
    for scout in scouts:
        scout = discover(scout, graph, n)
        new_scouts.put(scout)


def add_best_scouts(scouts, best_scouts):
    for scout in best_scouts:
        scouts.put(scout)


def main():
    graph = generate_rand_graph()

    # generate initial scouts
    scouts = PriorityQueue()
    generate_scouts(graph, scouts, SCOUTS_N)

    for i in range(2000):
        if not i % 20:
            best = scouts.get()
            print(f"Iteration {i}, min f: {best.f}")
            scouts.put(best)

        # find the best scouts and remaining scouts
        best_scouts = find_best_scouts(scouts)
        random_scouts = scouts.queue

        # perform local search
        scouts = PriorityQueue()
        local_search(graph, scouts, best_scouts, BEST_FORAGERS_N)
        local_search(graph, scouts, random_scouts, RANDOM_FORAGERS_N)

        # save best solutions, look for new solutions
        best_scouts = find_best_scouts(scouts)
        scouts = PriorityQueue()
        generate_scouts(graph, scouts, RANDOM_SCOUTS_N)
        add_best_scouts(scouts, best_scouts)

    best = scouts.get()
    coloring = {k: v for k, v in sorted(best.coloring.items(), key=lambda item: item[0])}
    print(f"Best coloring function: {best.f}\nColoring: {coloring}")


if __name__ == "__main__":
    main()
