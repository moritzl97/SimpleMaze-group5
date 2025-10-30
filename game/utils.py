# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

import os
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
    banner = r"""
    .-=~=-.                                                                 .-=~=-.
    (__  _)-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-(__  _)
    ( _ __)                                                                 ( _ __)
    (__  _)                                                                 (__  _)
    ( _ __)                                                                 ( _ __)
    (_ ___)-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-(_ ___)
    `-._.-'                                                                 `-._.-'"""
    print(banner[:296 - int(room_name_len / 2)] + Color.bold + room_display_name + Color.end + banner[
        296 + math.ceil(room_name_len / 2):])