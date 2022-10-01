from buffered_sorter import BufferedSorter


def main():
    sorter = BufferedSorter("a.bin", "b.bin", "c.bin", 1024**2//8)
    sorter.copy_from_file("32Gb.bin")
    sorter.sort()
    print(sorter)


if __name__ == "__main__":
    main()
