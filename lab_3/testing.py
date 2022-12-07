from btree import BTree

if __name__ == "__main__":
    tree = BTree(25)
    tree.insert_random_values()
    tree.start_testing()
