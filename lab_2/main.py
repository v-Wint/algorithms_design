from tester import Tester


def main():
    tester = Tester()
    # tester.create_mazes()
    tester.test_ldfs()
    tester.test_astar()


if __name__ == "__main__":
    main()
