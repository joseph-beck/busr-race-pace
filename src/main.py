import curses
from app import run
from graphs import make_average_race_pace


def main():
    curses.wrapper(run)

if __name__ == '__main__':
    main()
