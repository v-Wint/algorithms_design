import func_timeout
import os
import psutil


class LDFSSearcher:
    def __init__(self):
        self.it = 0  # number of iterations used
        self.st = 0  # number of states used
        self.max_stack = 0  # maximum simultaneous states at a time
        self.stops = 0

    def search(self, m, limit):
        return func_timeout.func_timeout(30*60, self._search, args=[m, limit])  # limit time of search to 30

    def _search(self, m, limit):
        self.it = 0
        self.max_stack = 0
        self.stops = 0

        start = (m.rows, m.cols)
        stack = [(start, [start])]
        states = []
        while stack:
            if psutil.Process(os.getpid()).memory_info().rss > 1024**3:  # limit memory use to 1 Gb
                raise MemoryError("1 Gb memory exceeded")
            self.it += 1
            if len(stack) > self.max_stack:  # check if stack len exceeds current max
                self.max_stack = len(stack)

            curr, path = stack.pop()
            if curr not in states:  # just to track
                states.append(curr)
            if len(path) - 1 == limit:
                self.stops += 1
                continue
            if curr == (1, 1):
                self.st = len(states)
                return path
            stack += self._expand(m, curr, path)
        self.st = len(states)
        return []

    @staticmethod
    def _expand(m, curr, path):
        directions = {"E": lambda x: (x[0], x[1] + 1),
                      "W": lambda x: (x[0], x[1] - 1),
                      "N": lambda x: (x[0] - 1, x[1]),
                      "S": lambda x: (x[0] + 1, x[1])}
        neighbours = []
        for d in "ENSW":
            if m.maze_map[curr][d]:
                neighbour = directions[d](curr)
                if neighbour not in path:
                    neighbours += (neighbour, path + [neighbour]),
        return neighbours

    def classic_search(self, m, limit):
        """Algorithm with no features tracked"""
        start = (m.rows, m.cols)
        stack = [(start, [start])]
        while stack:
            curr, path = stack.pop()
            if len(path) - 1 == limit:
                continue
            if curr == (1, 1):
                return path
            stack += self._expand(m, curr, path)
        return []
