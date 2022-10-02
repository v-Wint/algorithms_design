from buffered_sorter import BufferedSorter


def main():
    sorter = BufferedSorter("a.bin", "b.bin", "c.bin", 1024**3//8)
    sorter.copy_from_file("32GBFILE.bin")
    sorter.buffered_sort()


if __name__ == "__main__":
    main()
