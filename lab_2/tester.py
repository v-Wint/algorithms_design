from ldfs_searcher import LDFSSearcher
from a_star_searcher import AStarSearcher
from pyamaze import maze, agent
import os
import time


class Tester:
    def __init__(self):
        self.ldfs = LDFSSearcher()
        self.astar = AStarSearcher()

    @staticmethod
    def create_mazes(x=20, y=20, loop_percent=15, n=20):
        for _ in range(n):
            m = maze(x, y)
            m.CreateMaze(loopPercent=loop_percent, saveMaze=True)
            time.sleep(1)

    def test_ldfs(self, directory="states/", n=20):
        it = 0
        st = 0
        max_st = 0
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            m = maze()
            m.CreateMaze(loadMaze=path)
            self.ldfs.search(m, m.rows*m.cols//3)
            print(f"Maze {m.rows}x{m.cols}\n"
                  f"Iterations: {self.ldfs.it}, n of states: {self.ldfs.st}, max stack len: {self.ldfs.max_stack}\n")
            it += self.ldfs.it
            st += self.ldfs.st
            max_st += self.ldfs.max_stack
        print(f"Average iterations: {it/n}\n"
              f"Average n of states: {st/n}\n"
              f"Average max stack: {max_st/n}\n")

    def test_astar(self, directory="states/", n=20):
        it = 0
        st = 0
        max_st = 0
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            m = maze()
            m.CreateMaze(loadMaze=path)
            self.astar.search(m)
            print(f"Maze {m.rows}x{m.cols}\n"
                  f"Iterations: {self.astar.it}, n of states: {self.astar.st}, max stack len: {self.astar.max_stack}\n")
            it += self.astar.it
            st += self.astar.st
            max_st += self.astar.max_stack
        print(f"Average iterations: {it / n}\n"
              f"Average n of states: {st / n}\n"
              f"Average max stack: {max_st / n}\n")

    def search_ldfs(self, x=100, y=100, limit=0, loop_percent=15, print_result=False, show=False, save_maze=False):
        m = maze(x, y)
        m.CreateMaze(loopPercent=loop_percent, saveMaze=save_maze)
        limit = limit if limit else x*y//2
        path = self.ldfs.search(m, limit)
        print(f"Maze {x}x{y}, loopPercent={loop_percent}, show={show}\n"
              f"Iterations: {self.ldfs.it}, n of states: {self.ldfs.st}, max stack len: {self.ldfs.max_stack}\n")
        if print_result:
            print(f"Result: {path}\n")
        if show and path:
            a = agent(m, footprints=True, filled=True)
            m.tracePath({a: path}, delay=5)
            m.run()

    def search_astar(self, x=100, y=100, loop_percent=15, print_result=False, show=False, save_maze=False):
        m = maze(x, y)
        m.CreateMaze(loopPercent=loop_percent, saveMaze=save_maze)
        path = self.astar.search(m)
        print(f"Maze {x}x{y}, loopPercent={loop_percent}, show={show}\n"
              f"Iterations: {self.astar.it}, n of states: {self.astar.st}, max stack len: {self.astar.max_stack}\n")
        if print_result:
            print(f"Result: {path}\n")
        if show and path:
            a = agent(m, footprints=True, filled=True)
            m.tracePath({a: path}, delay=5)
            m.run()
