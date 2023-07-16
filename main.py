import curses
from src.app import run


def main():
    curses.wrapper(run)


if __name__ == '__main__':
    main()
