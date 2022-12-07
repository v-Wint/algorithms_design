import random


class Node:
    def __init__(self):
        self.keys = []
        self.child = []

    @property
    def leaf(self):
        return not self.child


class BTree:
    def __init__(self, t):
        self.t = t
        self.min_keys = t - 1
        self.max_keys = 2 * t - 1

        self.root = Node()

        self.comps = 0

    def insert(self, key):
        if len(self.root.keys) != self.max_keys:
            self._insert_in_node(self.root, key)
        else:
            new_root = Node()
            new_root.child.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self.insert(key)

    def _insert_in_node(self, node, key):
        # find index to be inserted
        i = len(node.keys) - 1
        while i >= 0 and node.keys[i][0] >= key[0]:
            i -= 1

        if node.leaf:
            node.keys.insert(i + 1, key)
        else:
            if len(node.child[i+1].keys) == self.max_keys:
                self._split_child(node, i + 1)
                if node.keys[i+1][0] < key[0]:
                    i += 1
            self._insert_in_node(node.child[i+1], key)

    def _split_child(self, parent, i):
        new_child = Node()
        half_max = self.max_keys // 2
        child = parent.child[i]
        middle = child.keys[half_max]

        new_child.keys = child.keys[half_max+1:]
        child.keys = child.keys[:half_max]

        if not child.leaf:
            new_child.child = child.child[half_max+1:]
            child.child = child.child[:half_max+1]

        parent.keys.insert(i, middle)
        parent.child.insert(i+1, new_child)

    def search(self, k):
        r = self._search_in_node(k, self.root)
        return r[-1][1:] if r else r

    def _search_in_node(self, k, node, parent=None):
        keys = list(node.keys)
        n = len(keys)
        if not n % 2:
            keys.append((float('inf'), 0))
            n += 1
        i = n // 2 + int(n % 2)  # ceil
        d = n // 2  # floor
        while d:
            self.comps += 1
            if keys[i - 1][0] == k:
                return node, parent, i-1, node.keys[i - 1]
            elif keys[i - 1][0] < k:
                i = i + d // 2 + int(d % 2)
            else:
                i = i - d // 2 - int(d % 2)
            d = d // 2
        if keys[i - 1][0] == k:
            self.comps += 1
            return node, parent, i-1, node.keys[i - 1]
        if node.leaf:
            return None
        else:
            if keys[i-1][0] > k:
                self.comps += 1
                return self._search_in_node(k, node.child[i-1], node)
            else:
                return self._search_in_node(k, node.child[i], node)

    def edit(self, key):
        r = self._search_in_node(key[0], self.root)
        if r:
            node, _, i, _ = r
            node.keys[i] = key
            return True
        else:
            return None

    def delete(self, k):
        r = self._search_in_node(k, self.root)
        if r:
            node, parent, _, _ = r
        else:
            return False

        i = self._delete_in_node(node, k)

        if node.leaf:
            if len(node.keys) < self.min_keys:  # if now number of keys violates properties
                i = parent.child.index(node)
                # if the left sibling exists and has enough keys, swap: left sibling -> parent -> node
                if i != 0 and len(parent.child[i-1].keys) > self.min_keys:
                    node.keys.insert(0, parent.keys.pop(i - 1))
                    parent.keys.insert(i - 1, parent.child[i - 1].keys.pop())
                else:
                    # if the right sibling exists and has enough keys, swap: right sibling -> parent -> node
                    if i != len(parent.child) - 1 and len(parent.child[i + 1].keys) > self.min_keys:
                        node.keys.append(parent.keys.pop(i))
                        parent.keys.insert(i, parent.child[i + 1].keys.pop(0))
                    # elif right sibling doesnt exist (and left sibling has not enough keys),
                    # merge node with left sibling
                    elif i == len(parent.child) - 1:
                        node.keys = parent.child[i - 1].keys + [parent.keys.pop(i - 1)] + node.keys
                        parent.child.pop(i - 1)

                    # else right sibling exists, but has not enough keys, merge with right sibling
                    else:
                        node.keys = node.keys + [parent.keys.pop(i)] + parent.child[i + 1].keys
                        parent.child.pop(i + 1)
        else:
            sibling = node.child[i]  # work with left sibling
            while not sibling.leaf:  # find the rightest descendant of the left sibling
                sibling = sibling.child[-1]

            if len(sibling.keys) > self.min_keys:  # if we can borrow a key, do it
                node.keys.insert(i, sibling.keys.pop())
            else:
                parent = node  # keep track of a parent
                sibling = node.child[i+1]  # work with right sibling
                while not sibling.leaf:  # find the leftest descendant of the right sibling
                    parent = sibling
                    sibling = parent.child[0]

                if len(sibling.keys) > self.min_keys:  # if can borrow, do it
                    node.keys.insert(i, sibling.keys.pop(0))
                else:
                    if parent == node:  # if the immediate right sibling of node is leaf, merge the left and right
                        node.child[i].keys += node.child[i+1].keys
                        node.child[i].child += node.child[i+1].child
                        node.child.pop(i+1)
                    else:
                        node.keys.insert(i, sibling.keys.pop(0))
                        # if the leftest descendant of right sibling has not enough keys and the descendant which comes
                        # after him has enough keys, swap: child[1] -> parent -> child[0]
                        if len(parent.child[1].keys) > self.min_keys:
                            sibling.keys.append(parent.keys.pop(0))
                            parent.keys.insert(i, parent.child[1].keys.pop(0))
                        else:  # else merge them two
                            sibling.keys = sibling.keys + [parent.keys.pop(0)] + parent.child[1].keys
                            parent.child.pop(1)
        return True

    def _delete_in_node(self, node, k):
        for i, key in enumerate(node.keys):
            if key[0] == k:
                node.keys.pop(i)
                return i

    def __repr__(self):
        def _print(x, l):
            r = "\t" * l + str([a[0] for a in x.keys])[1:-1] + "\n"
            for child in x.child:
                r += _print(child, l+1)
            return r
        return _print(self.root, 0)

    def insert_random_values(self):
        values = list(range(10_000))
        random.shuffle(values)
        for value in values:
            self.insert((value, float('inf')))

    def start_testing(self):
        for i in range(1, 11):
            self.search(100*i)
            print(f"Search number: {i}\nComparisons: {self.comps}")
            self.comps = 0
