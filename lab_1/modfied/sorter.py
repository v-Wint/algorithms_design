from random import randint
import shutil


class Reader:
    """Class representing a binary file and two reading pointers: current and next"""
    def __init__(self, path: str):
        self.path = path
        self.f = open(path, "rb")
        self.curr = self.f.read(32)
        self.next = self.f.read(32)

    def close(self):
        self.f.close()

    def __iter__(self):
        return self

    def __next__(self):
        """Return current pointer and moves pointers forward by 1"""
        tmp = self.curr
        self.curr = self.next
        self.next = self.f.read(32)
        return tmp


class Sorter:
    def __init__(self, path_a: str, path_b: str, path_c: str):
        """File B and C is cleared, file A is not"""
        self.path_a = path_a
        self.path_b = path_b
        self.path_c = path_c
        self._clear(path_b)
        self._clear(path_c)

    def create_random_file(self, n: int, max_n: int):
        with open(self.path_a, "wb") as a:
            for i in range(n):
                a.write(randint(1, max_n).to_bytes(32, byteorder="big"))

    def copy_from_file(self, path: str):
        shutil.copy(path, self.path_a)

    def sort(self):
        while not self._is_sorted():
            self._distribute()
            self._merge()

    def __str__(self):
        a, b, c = "A: " + self._read(self.path_a), "B: " + self._read(self.path_b), "C: " + self._read(self.path_c)
        return "\n".join([x for x in [a, b, c] if x])

    def _distribute(self):
        a = Reader(self.path_a)
        b = open(self.path_b, "wb")
        c = open(self.path_c, "wb")

        i = True
        while a.curr:
            b.write(a.curr) if i else c.write(a.curr)
            if a.curr > a.next:
                i = not i
            next(a)

        a.close(), b.close(), c.close()

    def _merge(self):
        """
        Злиття відповідних серій
        Логіка наступна:
            Якщо обидва дані числа не в кінці серії, ми знаходимо менше, його дописуємо, і посуваємо
            покажчик, таким чином зливаючи ці дві серії
            Інакше якщо число файлу В в кінці серії, то ми дозливаємо актуальну серію файла В і залишки
            серії файла С, тобто якщо число із файла С менше, ми його дописуємо, як тільки меншим
            виявиться оце наше останнє число серії із файла В, то ми це число дописуємо, і всі інші
            числа із серії із файла С так само дописуємо аж до кінця серії. Після цієї операції обидва
            покажчика будуть на початку нової серії
            Аналогічно робимо якщо число файлу С в кінці серії
            Якщо ж обидва числа в кінці серії, дописуємо їх по зростанню і суваємо покажчик на крок уперед,
            в результаті обидва покажчики на початку серії
            Якщо в кінці фалу, дописуємо залишок іншого файлу
        """
        a = open(self.path_a, "wb")
        b = Reader(self.path_b)
        c = Reader(self.path_c)
        while b.curr and c.curr:
            if b.curr <= b.next and c.curr <= c.next:
                if b.curr <= c.curr:
                    a.write(next(b))
                else:
                    a.write(next(c))
            elif b.curr >= b.next and c.curr <= c.next:
                while c.curr <= c.next:
                    if b.curr <= c.curr:
                        a.write(next(b))
                        while c.curr <= c.next:
                            a.write(next(c))
                        a.write(next(c))
                        break
                    else:
                        a.write(next(c))
            elif c.curr >= c.next and b.curr <= b.next:
                while b.curr <= b.next:
                    if c.curr <= b.curr:
                        a.write(next(c))
                        while b.curr <= b.next:
                            a.write(next(b))
                        a.write(next(b))
                        break
                    else:
                        a.write(next(b))
            else:
                if c.curr <= b.curr:
                    a.write(c.curr)
                    a.write(b.curr)
                else:
                    a.write(b.curr)
                    a.write(c.curr)
                next(c), next(b)

        if not b.curr and c.curr:
            while c.curr:
                a.write(next(c))
        elif not c.curr and b.curr:
            while b.curr:
                a.write(next(b))

        a.close(), b.close(), c.close()

    def _is_sorted(self):
        """Check if file A is already sorted"""
        a = Reader(self.path_a)
        while a.next:
            if a.curr > a.next:
                a.close()
                return False
            next(a)
        a.close()
        return True

    @staticmethod
    def _read(path: str) -> str:
        """Read the first 30 numbers from a file placing '|' in the end of each series"""
        s = ""
        f = Reader(path)

        for _ in range(30):
            if not f.curr:
                break
            s += str(int.from_bytes(f.curr, byteorder="big")) + " "
            if f.curr > f.next:
                s += "| "
            next(f)

        f.close()
        return s

    @staticmethod
    def _clear(path: str):
        with open(path, "wb"):
            pass
