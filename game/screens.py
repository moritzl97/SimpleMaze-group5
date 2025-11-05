# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

import sys
import time

from game.db import list_saves, delete_save
from game.basic_commands import display_scoreboard, handle_quit
from game.db_utils import *
from game.utils import *
import pygame

def main_menu(state):
    title_music = pygame.mixer.Sound(resource_path('assets/HolFix - Mystery.mp3'))
    title_music.play(loops=-1)
    while True:
        title_music.set_volume(state["volume"])
        clear_screen()
        print_and_center(r""" _______  _______  _______  _______  _______  _______ 
(  ____ \(  ____ \(  ____ \(  ___  )(  ____ )(  ____ \
| (    \/| (    \/| (    \/| (   ) || (    )|| (    \/
| (__    | (_____ | |      | (___) || (____)|| (__    
|  __)   (_____  )| |      |  ___  ||  _____)|  __)   
| (            ) || |      | (   ) || (      | (      
| (____/\/\____) || (____/\| )   ( || )      | (____/\
(_______/\_______)(_______/|/     \||/       (_______/""")
        print_and_center(r""" ____  _____   _____ _     _____
/  _ \/    /  /__ __Y \ /|/  __/
| / \||  __\    / \ | |_|||  \  
| \_/|| |       | | | | |||  /_ 
\____/\_/       \_/ \_/ \|\____\
""", end="")
        print(Color.red, end="")
        print_and_center(r"""
 _       _________ _______          _________ _______  _______  _______  _______ 
( (    /|\__   __/(  ____ \|\     /|\__   __/(       )(  ___  )(  ____ )(  ____ \
|  \  ( |   ) (   | (    \/| )   ( |   ) (   | |) (| || (   ) || (    )|| (    \/
|   \ | |   | |   | |      | (___) |   | |   | ||_|| || (___) || (____)|| (__    
| (\ \) |   | |   | | ____ |  ___  |   | |   | |   | ||  ___  ||     __)|  __)   
| | \   |   | |   | | \_  )| (   ) |   | |   | |   | || (   ) || (\ (   | (      
| )  \  |___) (___| (___) || )   ( |   | |   | )   ( || )   ( || ) \ \__| (____/\
|/    )_)\_______/(_______)|/     \|   )_(   |/     \||/     \||/   \__/(_______/""")
        print(Color.end, end="")
        space = "   "
        print_and_center("Start new game" + space + "Load game" + space + "Delete save" + space + "Scoreboard" + space + "Achievements" + space + "Credits" + space + "Options" + space + "Exit game")
        # start game
        # load game
        # highscores
        # credits

        command = input("").strip().lower()

        if command == "start new game" or command == "start" or command == "start game" or command == "new game":
            title_music.stop()
            return None
        elif command == "load game" or command == "load":
            #load game
            clear_screen()
            save_id = load_menu(state)
            if save_id:
                title_music.stop()
                return save_id
        elif command == "scoreboard":
            # call status command
            clear_screen()
            display_scoreboard(state)
            input("")
        elif command == "options":
            # open option screen
            clear_screen()
            options_menu(state)
        elif command == "credits":
            clear_screen()
            credits_screen()
            input("")
        if command == "achievements":
            clear_screen()
            achievement_screen(state)
            input("")
        elif command in ["exit game", "exit", "quit"]:
            # call exit function
            state["db_conn"].close()
            sys.exit()
        elif command.startswith("delete"):
            # load game
            clear_screen()
            delete_menu(state)


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
    print("")
    print("Congratulations! You escaped the nightmare!".center(82))
    time_delta = datetime.timedelta(seconds=db_get_elapsed_time(state))
    total_seconds = int(time_delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_formatted = f"{hours}:{minutes:02}:{seconds:02}"
    print(f"You completed the game in {time_formatted}".center(82))
    achievements = db_get_all_achievements_of_a_save(state, state["save_id"])
    if achievements:
        print("")
        print("You have gained the following achievements:".center(82))
        print(f"{' '.join(achievements)}".center(82))
    input("").strip().lower()
    return

def credits_screen():
    print_and_center(r"""  ____              _   _       
 / ___|_ __ ___  __| (_) |_ ___ 
| |   | '__/ _ \/ _` | | __/ __|
| |___| | |  __/ (_| | | |_\__ \
 \____|_|  \___|\__,_|_|\__|___/""")
    print_and_center("Escape of the Nightmare was created by:")
    print("#" + "-" * 80 + "#")
    print_and_center("""   Moritz Lackner    
    Oskar Lukáč      
 Dominika Nowakiewicz
   Mihail Petrov     
  Rodrigo Polo Lopez 
    Tieme van Rees   """)
    print("#" + "-" * 80 + "#")
    print_and_center("""This student project was created as part of the application\ndevelopment course at The Hague University of Applied Sciences.""")
    print("#" + "-" * 80 + "#")
    print_and_center("""Music and Sound Effect by
Stronger Together by Nicolas Gasparini (Myuu)
Mystery by HolFix
Sound effect by LordSonny from Pixabay""")
    print("#" + "-" * 80 + "#")
    return

def achievement_screen(state):
    achievement_list = db_get_all_achievements(state)
    print_and_center(r"""
    _        _     _                                     _       
   / \   ___| |__ (_) _____   _____ _ __ ___   ___ _ __ | |_ ___ 
  / _ \ / __| '_ \| |/ _ \ \ / / _ \ '_ ` _ \ / _ \ '_ \| __/ __|
 / ___ \ (__| | | | |  __/\ V /  __/ | | | | |  __/ | | | |_\__ \
/_/   \_\___|_| |_|_|\___| \_/ \___|_| |_| |_|\___|_| |_|\__|___/""")
    print("#" + "-"* 80 + "#")
    for item in achievement_list:
        if not item[2]:
            player_percent = 0
        else:
            player_percent = item[2]
        icon = item[0]
        description = item[1]
        print(f"               {int(player_percent):>4}%    {icon}    {description.ljust(30)}")
    print("#" + "-"* 80 + "#")
    print("Percentages represent players who have unlocked the achievement.".center(82))
    return

def load_menu(state):
    conn = state["db_conn"]
    print_and_center(r"""
 _                    _   ____                  
| |    ___   __ _  __| | / ___|  __ ___   _____ 
| |   / _ \ / _` |/ _` | \___ \ / _` \ \ / / _ \
| |__| (_) | (_| | (_| |  ___) | (_| |\ V /  __/
|_____\___/ \__,_|\__,_| |____/ \__,_| \_/ \___|""")
    print("")
    rows = list_saves(conn)  # [(save_id, player_name, current_room, saved_at), ...]
    print("#" + "-" * 80 + "#")
    if not rows:
        print("There are no saves yet.")
        time.sleep(2)
        return None

    # Print save list
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
        achievements = db_get_all_achievements_of_a_save(state, save_id)
        print(f"   {row_number+1:>3}. {name:<12} In {last_room.replace('_', ' ').title():<18} Last saved at {date_only} {time_only} {' '.join(achievements)}")
    print("#" + "-" * 80 + "#")
    print("")

    # Input loop
    while True:
        choice = input("Enter a number of the save you want to load or 'back' to go to the main menu: ").strip().lower()
        if choice.lower() == "back":
            return None

        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a valid number or 'back'.")
            continue

        if 0 < choice <= len(rows):
            save_id = rows[choice-1][0]
            return save_id
        else:
            print("Please enter a valid number or 'back'.")

def delete_menu(state):
    conn = state["db_conn"]
    print_and_center(r"""
 ____       _      _         ____                  
|  _ \  ___| | ___| |_ ___  / ___|  __ ___   _____ 
| | | |/ _ \ |/ _ \ __/ _ \ \___ \ / _` \ \ / / _ \
| |_| |  __/ |  __/ ||  __/  ___) | (_| |\ V /  __/
|____/ \___|_|\___|\__\___| |____/ \__,_| \_/ \___|""")
    print("")
    rows = list_saves(conn)  # [(save_id, player_name, current_room, saved_at), ...]
    print("#" + "-" * 80 + "#")
    if not rows:
        print("There are no saves yet.")
        time.sleep(2)
        return

    # Print save list
    for row_number, (save_id, name, last_room, saved_at) in enumerate(rows):
        # SQLite timestamps look like: "2025-02-12 10:33:11"
        timestamp = datetime.datetime.strptime(saved_at, "%Y-%m-%d %H:%M:%S")

        date_only = timestamp.strftime("%d-%m-%Y")
        time_only = timestamp.strftime("%H:%M:%S")
        achievements = db_get_all_achievements_of_a_save(state, save_id)
        print(f"   {row_number+1:>3}. {name:<12} In {last_room.replace('_', ' ').title():<18} Last saved at {date_only} {time_only} {' '.join(achievements)}")
    print("#" + "-" * 80 + "#")
    print("")

    # Input loop
    while True:
        choice = input("Enter a number of the save you want to delete or 'back' to go to the main menu: ").strip().lower()
        if choice.lower() == "back":
            return
        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a valid number or 'back'.")
            continue

        if 0 < choice <= len(rows):
            save_id = rows[choice-1][0]
            break
        else:
            print("Please enter a valid number or 'back'.")

    timestamp = datetime.datetime.strptime(rows[choice-1][3], "%Y-%m-%d %H:%M:%S")
    date_only = timestamp.strftime("%d-%m-%Y")
    time_only = timestamp.strftime("%H:%M:%S")
    achievements = db_get_all_achievements_of_a_save(state, save_id)
    print(f"   {choice:>3}. {rows[choice-1][1]:<12} In {rows[choice-1][2].replace('_', ' ').title():<18} Last saved at {date_only} {time_only} {' '.join(achievements)}")
    print("Are you sure you want to delete this save? (y/n)")
    print("Warning this is not reversible and will also delete the earned achievements with this save.")
    conformation = input("").strip().lower()
    if conformation in ["yes", "y"]:
        delete_save(state, save_id)
    else:
        print("Nothing was deleted.")
    time.sleep(2)
    return

def options_menu(state):
        conn = state["db_conn"]
        print_and_center(r"""
  ___        _   _                 
 / _ \ _ __ | |_(_) ___  _ __  ___ 
| | | | '_ \| __| |/ _ \| '_ \/ __|
| |_| | |_) | |_| | (_) | | | \__ \
 \___/| .__/ \__|_|\___/|_| |_|___/
      |_|                          """)
        print("")
        volume = int(state["volume"]*100/0.25)
        print_and_center(f"Volume    {volume:3}")
        print_and_center(f"Back         ")

        # Input loop
        while True:
            choice = input("").strip().lower()
            if choice == "back":
                return
            elif choice.startswith("volume"):
                try:
                    choice = int(choice[7:])
                except ValueError:
                    print("To change the volume enter 'Volume <number>' with a number between 0 and 100.")
                    continue
                choice = min(max(choice, 0), 100)
                state["volume"] = 0.25 * choice/100
                return

def pause_menu(state, game_music):
    # pause the game and timer
    db_update_elapsed_time(state)

    elapsed_seconds = db_get_elapsed_time(state)
    time_delta = datetime.timedelta(seconds=elapsed_seconds)
    total_seconds = int(time_delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_formatted = f"{hours}:{minutes:02}:{seconds:02}"

    while True:
        clear_screen()
        print_and_center(r"""
 _______  _______           _______  _______ 
(  ____ )(  ___  )|\     /|(  ____ \(  ____ \
| (    )|| (   ) || )   ( || (    \/| (    \/
| (____)|| (___) || |   | || (_____ | (__    
|  _____)|  ___  || |   | |(_____  )|  __)   
| (      | (   ) || |   | |      ) || (      
| )      | )   ( || (___) |/\____) || (____/\
|/       |/     \|(_______)\_______)(_______/""")

        print_and_center(time_formatted)
        space = "     "
        print_and_center("Resume" + space + "Options" + space + "Quit  ")

        command = input("").strip().lower()
        if command == "resume":
            state["start_time"] = time.time() - db_get_elapsed_time(state)
            print("Game resumed.")
            return None
        elif command == "quit":
            quit_flag = handle_quit(state)
            return quit_flag
        elif command == "options":
            clear_screen()
            options_menu(state)
            game_music.set_volume(state["volume"])