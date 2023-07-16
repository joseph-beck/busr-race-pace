from ui import select_option, select_file, show_selected_file, show_selected_option
from graphs import make_continuous_race_pace, make_average_race_pace


def run(stdscr):
    options = ['Race Pace', 'Average Race Pace']
    option = select_option(stdscr, options)
    show_selected_option(stdscr, option)

    dir = 'races'
    selected = select_file(stdscr, dir)
    show_selected_file(stdscr, selected)

    if option == 'Race Pace':
        make_continuous_race_pace(selected)
    elif option == 'Average Race Pace':
        make_average_race_pace(selected)
    