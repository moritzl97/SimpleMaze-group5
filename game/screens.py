# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

import sys
from game.db import list_saves, delete_save
from game.basic_commands import display_scoreboard
import datetime

from game.db_utils import db_get_elapsed_time
from game.utils import *
import time

def main_menu(state):
    while True:
        clear_screen()
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
        print(Color.red + r"""
     _       _________ _______          _________ _______  _______  _______  _______ 
    ( (    /|\__   __/(  ____ \|\     /|\__   __/(       )(  ___  )(  ____ )(  ____ \
    |  \  ( |   ) (   | (    \/| )   ( |   ) (   | |) (| || (   ) || (    )|| (    \/
    |   \ | |   | |   | |      | (___) |   | |   | ||_|| || (___) || (____)|| (__    
    | (\ \) |   | |   | | ____ |  ___  |   | |   | |   | ||  ___  ||     __)|  __)   
    | | \   |   | |   | | \_  )| (   ) |   | |   | |   | || (   ) || (\ (   | (      
    | )  \  |___) (___| (___) || )   ( |   | |   | )   ( || )   ( || ) \ \__| (____/\
    |/    )_)\_______/(_______)|/     \|   )_(   |/     \||/     \||/   \__/(_______/""" + Color.end)
        space = "    "
        print(
            "            Start new game" + space + "Load game" + space + "Highscores" + space + "Credits" + space + "Exit game")
        # start game
        # load game
        # highscores
        # credits

        command = input("").strip().lower()

        if command == "start new game" or command == "start" or command == "start game" or command == "new game":
            return None
        elif command == "load game" or command == "load":
            #load game
            clear_screen()
            save_id = load_menu(state)
            if save_id:
                return save_id
        elif command == "highscores":
            # call status command
            clear_screen()
            display_scoreboard()
            input("")
        elif command == "credits":
            clear_screen()
            credits_screen()
            input("")
        elif command == "exit game" or command == "exit":
            # call exit function
            sys.exit()
        elif command.startswith("delete "):
            # delete save
            clear_screen()
            save_id = int(command[7:])
            delete_save(state, save_id)
            time.sleep(2)

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
    print("\n           Congratulations! You escaped the nightmare!")
    print(f"                You completed the game in {db_get_elapsed_time(state)}")
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
    return

def load_menu(state):
    conn = state["db_conn"]
    print(r"""
                     ____                       
                    / ___|  __ ___   _____  ___ 
                    \___ \ / _` \ \ / / _ \/ __|
                     ___) | (_| |\ V /  __/\__ \
                    |____/ \__,_| \_/ \___||___/""")
    print("\n")

    rows = list_saves(conn)  # [(save_id, player_name, current_room, saved_at), ...]

    if not rows:
        print("There are no saves yet.")
        time.sleep(2)
        return None

    # Print save list
    print("Available saves:\n")
    for row_number, (save_id, name, last_room, saved_at) in enumerate(rows):
        # SQLite timestamps look like: "2025-02-12 10:33:11"
        try:
            timestamp = datetime.datetime.strptime(saved_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # fallback for ISO8601 if the first doesn't work
            try:
                timestamp = datetime.datetime.fromisoformat(saved_at)
            except Exception:
                timestamp = datetime.datetime.now()

        date_only = timestamp.strftime("%d-%m-%Y")
        time_only = timestamp.strftime("%H:%M:%S")
        print(f"{row_number+1}. {name}: In {last_room or 'unknown room'}, saved at {date_only} {time_only}")
    print("")

    # Input loop
    while True:
        choice = input("Enter a number of the save you want to load or 'back' to go to the main menu.").strip()
        if choice.lower() == "back":
            return None

        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a valid number or 'back'.")

        if choice <= len(rows):
            save_id = rows[choice-1][0]
            return save_id
        else:
            print("Please enter a valid number or 'back'.")