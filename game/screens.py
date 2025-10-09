# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

import sys
from game.db import list_saves, load_state
from game.basic_commands import display_scoreboard

from game.utils import clear_screen
import os

def title_screen(conn):
    print(r"""
                _______  _______  _______  _______  _______  _______ 
               (  ____ \(  ____ \(  ____ \(  ___  )(  ____ )(  ____ \
               | (    \/| (    \/| (    \/| (   ) || (    )|| (    \/
               | (__    | (_____ | |      | (___) || (____)|| (__    
               |  __)   (_____  )| |      |  ___  ||  _____)|  __)   
               | (            ) || |      | (   ) || (      | (      
               | (____/\/\____) || (____/\| )   ( || )      | (____/\
               (_______/\_______)(_______/|/     \||/       (_______/""", end="")
    print(r"""
                           ____  _____   _____ _     _____
                          /  _ \/    /  /__ __Y \ /|/  __/
                          | / \||  __\    / \ | |_|||  \  
                          | \_/|| |       | | | | |||  /_ 
                          \____/\_/       \_/ \_/ \|\____\ """, end="")
    print("\033[31m" + r"""
     _       _________ _______          _________ _______  _______  _______  _______ 
    ( (    /|\__   __/(  ____ \|\     /|\__   __/(       )(  ___  )(  ____ )(  ____ \
    |  \  ( |   ) (   | (    \/| )   ( |   ) (   | |) (| || (   ) || (    )|| (    \/
    |   \ | |   | |   | |      | (___) |   | |   | ||_|| || (___) || (____)|| (__    
    | (\ \) |   | |   | | ____ |  ___  |   | |   | |   | ||  ___  ||     __)|  __)   
    | | \   |   | |   | | \_  )| (   ) |   | |   | |   | || (   ) || (\ (   | (      
    | )  \  |___) (___| (___) || )   ( |   | |   | )   ( || )   ( || ) \ \__| (____/\
    |/    )_)\_______/(_______)|/     \|   )_(   |/     \||/     \||/   \__/(_______/""" + "\033[0m")
    space = "    "
    print("          Start game" + space + "Load game" + space + "Highscores" + space + "Credits" + space + "Exit game")
    # start game
    # load game
    # highscores
    # credits
    while True:

        command = input("").strip().lower()

        if command == "start game" or command == "start":
            clear_screen()
            return None
        elif command == "load game" or command == "load":
            #load game
            save_state = load_menu(conn)
            if save_state:
                return save_state
        elif command == "highscores":
            # call status command
            display_scoreboard()
        elif command == "credits":
            credits_screen()
        elif command == "exit game" or command == "exit":
            # call exit function
            sys.exit()


def end_screen(state):
    # end
    clear_screen()
    print(r"""
                    _______  _        ______  
                    (  ____ \( (    /|(  __  \ 
                    | (    \/|  \  ( || (  \  )
                    | (__    |   \ | || |   ) |
                    |  __)   | (\ \) || |   | |
                    | (      | | \   || |   ) |
                    | (____/\| )  \  || (__/  )
                    (_______/|/    )_)(______/ 
    """)
    print("\n Congratulations! You escaped the nightmare!")
    print(f"You completed the game in {state['elapsed_time']}")
    input("").strip().lower()
    return

def credits_screen():
    # credits
    clear_screen()
    print("""\n\n\n\n
             Escape of the Nightmare was created by:
#-------------------------------------------------------------#
                        Moritz Lackner
                         Oskar Lukáč
                      Dominika Nowakiewicz
                        Mihail Petrov
                       Rodrigo Polo Lopez
                         Tieme van Rees
#-------------------------------------------------------------#
This student project was created as part of the application 
development course at The Hague University of Applied Sciences.\n\n\n\n
""")
    input("").strip().lower()
    return

def load_menu(conn):
    rows = list_saves(conn) # [(player_name, current_room, updated_at), ...]
    if not rows:
        print("No saves found.")
        return None
    print("Saves:")
    for row in rows:
        print(row)

    while True:
        choice = input("Enter player name of the save you want to load: ").strip()
        loaded = load_state(conn, choice)
        if not loaded:
            print("Save not found. Enter a valid player name.")
        else:
            print(f"Loaded {choice}. Resuming in '{loaded.get('current_room', 'start')}'.")
            return loaded