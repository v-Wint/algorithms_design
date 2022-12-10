from main import run
import crossover, local, mutation


def test1():
    functions = {crossover.one_point: (0, 0, 0, 0), crossover.two_point: (0, 0, 0, 0), crossover.even: (0, 0, 0, 0)}
    for func in functions:
        print(func.__name__)
        a, b, c, stuck = 0, 0, 0, 0
        for i in range(10):
            print(i)
            res = run(func, mutation.rand_change_interval, local.add_rand_adj_node)
            a += res[0]
            b += res[1]
            c += res[2]
            if res[2] == 100000:
                stuck += 1

        functions[func] = (a / 10, b / 10, c / 10, stuck)

    for func, results in functions.items():
        print(func.__name__, ":", results[3], ":", results[0], results[1], results[2])


def test2():
    functions = {mutation.rand_change_one: (0, 0, 0, 0), mutation.rand_change_interval: (0, 0, 0, 0)}
    for func in functions:
        print(func.__name__)
        a, b, c, stuck = 0, 0, 0, 0
        for i in range(20):
            print(i)
            res = run(crossover.two_point, func, local.add_rand_adj_node)
            a += res[0]
            b += res[1]
            c += res[2]
            if res[2] == 100000:
                stuck += 1

        functions[func] = (a / 20, b / 20, c / 20, stuck)

    for func, results in functions.items():
        print(func.__name__, ":", results[3], ":", results[0], results[1], results[2])


def test3():
    functions = {local.add_rand_adj_node: (0, 0, 0, 0), local.add_adj_node_heuristic: (0, 0, 0, 0)}
    for func in functions:
        print(func.__name__)
        a, b, c, stuck = 0, 0, 0, 0
        for i in range(20):
            print(i)
            res = run(crossover.two_point, mutation.rand_change_one, func)
            a += res[0]
            b += res[1]
            c += res[2]
            if res[2] == 100000:
                stuck += 1

        functions[func] = (a / 20, b / 20, c / 20, stuck)

    for func, results in functions.items():
        print(func.__name__, ":", results[3], ":", results[0], results[1], results[2])


if __name__ == "__main__":
    test1()
