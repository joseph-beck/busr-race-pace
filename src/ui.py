import os
import curses


def list_files(stdscr, directory, selected_index):
    stdscr.clear()
    files = [file for file in os.listdir(directory) if not file.startswith('.')]
    for i, file in enumerate(files):
        if i == selected_index:
            stdscr.addstr(i, 0, f"> {file}", curses.A_REVERSE)
        else:
            stdscr.addstr(i, 0, f"  {file}")
    stdscr.refresh()


def select_file(stdscr, directory):
    files = [file for file in os.listdir(directory) if not file.startswith('.')]
    selected_index = 0
    key = 0

    try:
        while key != ord('\n'):  # Enter key
            stdscr.clear()
            list_files(stdscr, directory, selected_index)

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)
            elif key == curses.KEY_DOWN:
                selected_index = min(len(files) - 1, selected_index + 1)

        selected_file = os.path.join(directory, files[selected_index])
        return selected_file
    finally:
        curses.endwin()  # Close the curses window
