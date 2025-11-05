# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

import os
import sys
import math

def clear_screen():
    if os.getenv("PYCHARM_HOSTED"):
        print("\n" * 50)  # fallback for PyCharm
    else:
        os.system('cls' if os.name == 'nt' else 'clear')


class Color:
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[93m"
    blue = "\033[94m"
    gray = "\033[90m"
    orange = "\033[38;2;255;165;0m"
    purple = "\033[0;35m"
    silver = "\033[38;5;146m"
    bronze = "\033[38;5;166m"
    bold = "\033[1m"
    underline = "\033[4m"
    framed = "\033[51m"
    end = "\033[0m"


def print_room_entry_banner(room):
    room_display_name = room.replace("_", " ").title()
    room_name_len = len(room_display_name)
    banner = r""".-=~=-.                                                                 .-=~=-.
(__  _)-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-(__  _)
( _ __)                                                                 ( _ __)
(__  _)                                                                 (__  _)
( _ __)                                                                 ( _ __)
(_ ___)-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-(_ ___)
`-._.-'                                                                 `-._.-'"""
    banner_with_text = banner[:280 - int(room_name_len / 2)] + room_display_name + banner[280 + math.ceil(room_name_len / 2):]
    print_and_center(banner_with_text)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path here
        base_path = sys._MEIPASS
    except AttributeError:
        # When running in a normal Python environment, just use current dir
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def print_and_center(input_str, end="\n"):
    # try:
    #     width = os.get_terminal_size().columns
    # except OSError:
    #     width = 80
    width = 126

    lines = input_str.splitlines()
    for i, line in enumerate(lines):
        if i == len(lines) - 1:
            print(line.center(width), end=end)  # Use custom end for last line
        else:
            print(line.center(width))
