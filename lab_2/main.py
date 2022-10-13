from tester import Tester


def main():
    tester = Tester()
    tester.test_ldfs(20)
    tester.test_astar(20)


if __name__ == "__main__":
    main()
