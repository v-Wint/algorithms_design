import func_timeout, psutil, os


class LDFSSearcher:
    def __init__(self):
        self.it = 0  # number of iterations used
        self.st = 0  # number of states used
        self.max_stack = 0  # maximum simultaneous states at a time

    def search(self, m, limit):
        return func_timeout.func_timeout(30*60, self._search, args=[m, limit])  # limit time of search to 30

    def _search(self, m, limit):
        self.it = 0
        self.max_stack = 0

        start = (m.rows, m.cols)  # cell and level
        stack = [(start, 0)]
        visited = {}
        while stack:
            if psutil.Process(os.getpid()).memory_info().rss > 1024**3:  # limit memory use to 1 Gb
                raise MemoryError("1 Gb memory exceeded")
            self.it += 1
            if len(stack) > self.max_stack:  # check if stack len exceeds current max
                self.max_stack = len(stack)

            curr, c_l = stack.pop()
            if c_l == limit:
                continue
            if curr == (1, 1):
                visited[curr] = c_l
                self.st = len(visited)  # numbers of states == number of visited
                return self._reconstruct(visited)
            if curr in visited:
                continue
            visited[curr] = c_l
            stack += self._expand(m, curr, c_l)
        self.st = len(visited)
        return []

    @staticmethod
    def _expand(m, curr, c_l):
        directions = {"E": lambda x: (x[0], x[1] + 1),
                      "W": lambda x: (x[0], x[1] - 1),
                      "N": lambda x: (x[0] - 1, x[1]),
                      "S": lambda x: (x[0] + 1, x[1])}
        neighbours = []
        for d in "ENSW":
            if m.maze_map[curr][d]:
                neighbours += (directions[d](curr), c_l+1),
        return neighbours

    @staticmethod
    def _reconstruct(visited):
        c, c_l = visited.popitem()  # cell and level
        path = [c]
        n, n_l = visited.popitem()
        while visited:
            if c_l - n_l == 1:  # if delta levels == 1 means the very found path
                path += n,
                c, c_l = n, n_l
            n, n_l = visited.popitem()
        path += n,
        return list(reversed(path))

    def classic_search(self, m, limit):
        """Algorithm with no features tracked"""
        start = (m.rows, m.cols)
        stack = [(start, 0)]
        visited = {}
        while stack:
            curr, c_l = stack.pop()  # cell and level
            if c_l == limit:
                continue
            if curr == (1, 1):
                visited[curr] = c_l
                return self._reconstruct(visited)
            if curr in visited:
                continue
            visited[curr] = c_l
            stack += self._expand(m, curr, c_l)
        return []
