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
from datetime import datetime
from game.utils import clear_screen
import os
import time

def title_screen(conn):
    while True:
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
        print(
            "                Start new game" + space + "Load game" + space + "Highscores" + space + "Credits" + space + "Exit game")
        # start game
        # load game
        # highscores
        # credits

        command = input("").strip().lower()

        if command == "start new game" or command == "start" or command == "start game" or command == "new game":
            clear_screen()
            return None
        elif command == "load game" or command == "load":
            #load game
            save_state = load_menu(conn)
            if save_state:
                return save_state
        elif command == "highscores":
            # call status command
            clear_screen()
            display_scoreboard()
            input("")
            clear_screen()
        elif command == "credits":
            credits_screen()
        elif command == "exit game" or command == "exit":
            # call exit function
            sys.exit()


def end_screen(state):
    # end screen
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
    clear_screen()
    print(r"""
                     ____                       
                    / ___|  __ ___   _____  ___ 
                    \___ \ / _` \ \ / / _ \/ __|
                     ___) | (_| |\ V /  __/\__ \
                    |____/ \__,_| \_/ \___||___/""")
    print("\n")
    rows = list_saves(conn) # [(player_name, current_room, updated_at), ...]
    if not rows:
        print("There are no saves yet.")
        time.sleep(2)
        return None

    for row in rows:
        name = row[0]
        last_room = row[1]
        timestamp = datetime.strptime(row[2], '%Y-%m-%dT%H:%M:%S.%fZ')
        #timestamp = row[2].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        date_only = timestamp.strftime("%d-%m-%Y")
        time_only = timestamp.strftime("%H:%M:%S")
        print(f"{name}: In {last_room}, saved at {date_only} {time_only}")
    print("")

    while True:
        choice = input("Enter player name of the save you want to load or 'back' to go to the main menu: ").strip()
        if choice == "back":
            return

        loaded = load_state(conn, choice)
        if not loaded:
            print("Save not found. Enter a valid player name or 'back' to go to the main menu.")
        else:
            print(f"Loading {choice}. Resuming in '{loaded.get('current_room', 'start')}'.")
            time.sleep(2)
            return loaded