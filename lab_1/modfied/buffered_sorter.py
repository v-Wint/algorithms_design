from sorter import Sorter
import os
import math


class BufferedSorter(Sorter):
    def __init__(self, path_a: str, path_b: str, path_c: str, n: int):
        super().__init__(path_a, path_b, path_c)
        self.iteration = 0
        self.split_n = 1
        self.n = n
        try:
            self.iter_max = int(int(math.log2(os.stat(self.path_a).st_size // 32 // self.n))) + 1
        except ValueError:
            self.iter_max = 1

    def create_random_file(self, n: int, max_n: int):
        super().create_random_file(n, max_n)
        self.iter_max = int(int(math.log2(os.stat(self.path_a).st_size // 32 // self.n))) + 1

    def copy_from_file(self, path: str):
        super().copy_from_file(path)
        self.iter_max = int(int(math.log2(os.stat(self.path_a).st_size // 32 // self.n))) + 1

    def buffered_sort(self):
        """Around 2 * 32 * n of RAM used max while buffering"""
        self._buffered_prepare()
        for _ in range(self.iter_max):
            self._buffered_distribute()
            self._merge()
            self.iteration += 1

    def _buffered_prepare(self):
        """Read chunks from file A, write sorted chunks into temporary file, copy it to file A"""
        tmp = open("tmp", "wb")
        a = open(self.path_a, "rb")

        buffer = []
        for _ in range(self.n):
            x = a.read(32)
            if not x:
                break
            buffer += x,

        while buffer:
            buffer.sort()

            for x in buffer:
                tmp.write(x)

            del buffer
            buffer = []

            for _ in range(self.n):
                x = a.read(32)
                if not x:
                    break
                buffer += x,

        tmp.close()
        a.close()

        self.copy_from_file("tmp")
        os.remove("tmp")

    def _buffered_distribute(self):
        a = open(self.path_a, "rb")
        b = open(self.path_b, "wb")
        c = open(self.path_c, "wb")

        buffer = []
        for _ in range(self.n):
            x = a.read(32)
            if not x:
                break
            buffer += x,

        i = True
        j = 2
        while buffer:
            for x in buffer:
                b.write(x) if i else c.write(x)

            if j > self.split_n:
                i = not i
                j = 1
            j += 1

            del buffer
            buffer = []
            for _ in range(self.n):
                x = a.read(32)
                if not x:
                    break
                buffer += x,
        self.split_n *= 2
        a.close(), b.close(), c.close()
