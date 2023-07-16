from src.ui import select_file
from src.graphs import make_pace_graph


def run(stdscr):
    dir = 'races'
    selected = select_file(stdscr, dir)
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"You selected: {selected.removeprefix(f'{dir}/').removesuffix(f'.csv')}")
    stdscr.addstr(1, 0, f"Press enter to make graph!")
    stdscr.refresh()
    stdscr.getch()

    make_pace_graph(selected)
