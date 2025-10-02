# -----------------------------------------------------------------------------
# File: utils.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

import os

def clear_screen():
    if os.getenv("PYCHARM_HOSTED"):
        print("\n" * 50)  # fallback for PyCharm
    else:
        os.system('cls' if os.name == 'nt' else 'clear')


