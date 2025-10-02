import sys

from game.utils import clear_screen
import os

def title_screen():
    # start game
    # load game
    # highscores
    # credits
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
           (_______/\_______)(_______/|/     \||/       (_______/""",end="")
        print(r"""
                       ____  _____   _____ _     _____
                      /  _ \/    /  /__ __Y \ /|/  __/
                      | / \||  __\    / \ | |_|||  \  
                      | \_/|| |       | | | | |||  /_ 
                      \____/\_/       \_/ \_/ \|\____\ """, end="")
        print("\033[31m"+r"""
 _       _________ _______          _________ _______  _______  _______  _______ 
( (    /|\__   __/(  ____ \|\     /|\__   __/(       )(  ___  )(  ____ )(  ____ \
|  \  ( |   ) (   | (    \/| )   ( |   ) (   | |) (| || (   ) || (    )|| (    \/
|   \ | |   | |   | |      | (___) |   | |   | ||_|| || (___) || (____)|| (__    
| (\ \) |   | |   | | ____ |  ___  |   | |   | |   | ||  ___  ||     __)|  __)   
| | \   |   | |   | | \_  )| (   ) |   | |   | |   | || (   ) || (\ (   | (      
| )  \  |___) (___| (___) || )   ( |   | |   | )   ( || )   ( || ) \ \__| (____/\
|/    )_)\_______/(_______)|/     \|   )_(   |/     \||/     \||/   \__/(_______/"""+"\033[0m")
        space = "    "
        print("          Start game"+space+"Load game"+space+"Highscores"+space+"Credits"+space+"Exit game")
        command = input("").strip().lower()

        if command == "start game" or command == "start":
            clear_screen()
            return None
        elif command == "load game" or command == "load":
            #load game
            save_state = load_menu()
            if save_state:
                return save_state
        elif command == "highscores":
            # call status command
            pass
        elif command == "credits":
            end_screen()
        elif command == "exit game" or command == "exit":
            # call exit function
            sys.exit()

def pause_screen():
    clear_screen()
    print(r"""
_______  _______           _______  _______ 
(  ____ )(  ___  )|\     /|(  ____ \(  ____ \
| (    )|| (   ) || )   ( || (    \/| (    \/
| (____)|| (___) || |   | || (_____ | (__    
|  _____)|  ___  || |   | |(_____  )|  __)   
| (      | (   ) || |   | |      ) || (      
| )      | )   ( || (___) |/\____) || (____/\
|/       |/     \|(_______)\_______)(_______/
""")
    print("       Resume    Exit game")
    return

def end_screen():
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

def load_menu():
    while True:
        print("Select a save:")
        # TODO list save
        save_name = input("> ")
        # TODO load save
        save = {}
        if save_name:
            return save
        else:
            return None
