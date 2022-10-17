import func_timeout
import math
import os
import psutil
from queue import PriorityQueue


class AStarSearcher:
    def __init__(self):
        self.it = 0  # number of iterations used
        self.st = 0  # number of states used
        self.max_stack = 0  # maximum simultaneous states at a time

    def search(self, m):
        return func_timeout.func_timeout(30*60, self._search, args=[m]) # limit time of search to 30

    def _search(self, m):
        self.it = 0
        self.max_stack = 0

        start = (m.rows, m.cols)

        g_score = {cell: float('inf') for cell in m.grid}
        g_score[start] = 0

        f_score = {cell: float('inf') for cell in m.grid}
        f_score[start] = self.__h(start, (1, 1))

        open = PriorityQueue()
        open.put((self.__h(start, (1, 1)), start))

        came_from = {}
        states = []
        while not open.empty():
            if psutil.Process(os.getpid()).memory_info().rss > 1024**3:  # limit memory use to 1 Gb
                raise MemoryError("1 Gb memory exceeded")

            self.it += 1
            if open.qsize() > self.max_stack:  # check if stack len exceeds current max
                self.max_stack = open.qsize()

            curr = open.get()[1]
            if curr not in states:  # just to track
                states.append(curr)
            if curr == (1, 1):
                self.st = len(states)
                return self._reconstruct(came_from, start)
            for neighbour in self._expand(m, curr):
                tentative_g_score = g_score[curr] + 1
                tentative_f_score = tentative_g_score + self.__h(neighbour, (1, 1))

                if tentative_f_score < f_score[neighbour]:
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_f_score
                    open.put((tentative_f_score, neighbour))
                    came_from[neighbour] = curr
        self.st = len(states)
        return []

    @staticmethod
    def __h(a, b):
        return math.sqrt((a[0]-b[0])**2 + (a[1] - b[1])**2)

    @staticmethod
    def _expand(m, curr):
        directions = {"E": lambda x: (x[0], x[1] + 1),
                      "W": lambda x: (x[0], x[1] - 1),
                      "N": lambda x: (x[0] - 1, x[1]),
                      "S": lambda x: (x[0] + 1, x[1])}
        neighbours = []
        for d in "ENSW":
            if m.maze_map[curr][d]:
                neighbours += directions[d](curr),
        return neighbours

    @staticmethod
    def _reconstruct(came_from, start):
        path = {}
        curr = (1, 1)
        while curr != start:
            path[came_from[curr]] = curr
            curr = came_from[curr]
        return path

    def classic_search(self, m):
        """Algorithm with no features tracked"""
        start = (m.rows, m.cols)

        g_score = {cell: float('inf') for cell in m.grid}
        g_score[start] = 0

        f_score = {cell: float('inf') for cell in m.grid}
        f_score[start] = self.__h(start, (1, 1))

        open = PriorityQueue()
        open.put((self.__h(start, (1, 1)), start))

        came_from = {}

        while not open.empty():

            curr = open.get()[1]
            if curr == (1, 1):
                return self._reconstruct(came_from, start)

            for neighbour in self._expand(m, curr):
                tentative_g_score = g_score[curr] + 1
                tentative_f_score = tentative_g_score + self.__h(neighbour, (1, 1))

                if tentative_f_score < f_score[neighbour]:
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = tentative_f_score
                    open.put((tentative_f_score, neighbour))
                    came_from[neighbour] = curr

        return []
