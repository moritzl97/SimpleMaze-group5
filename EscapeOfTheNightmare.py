# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

import time
from rooms import *
from game.basic_commands import handle_basic_commands, handle_go, handle_admin_go
from game.screens import pause_menu, main_menu, end_screen, credits_screen, intro_screen
from game.db import init_db, create_new_save
from game.utils import *
from game.db_utils import *
import sqlite3
import os
import pygame

###################################################
# Main game
###################################################
def game_loop(save_id):
    # Handle loading of save or intro of new game

    # Check if there is a save id given or create a new state, if it is a new game
    if save_id:
        state["save_id"] = save_id
        state["start_time"] = time.time() - db_get_elapsed_time(state)
    else:
        # Ask player name
        while True:
            print("\n\n\n")
            print_and_center("Enter your name")
            print("")
            player_name = input(" " * 60).strip()
            if player_name == "" or len(player_name)<3 or len(player_name)>20 or " " in player_name:
                print_and_center("Please enter a valid username without spaces and with at least 3 and less than 20 characters.")
                time.sleep(2)
                clear_screen()
            else:
                break

        clear_screen()
        print("\n\n\n")
        print_and_center(f"Welcome to the Nightmare, {player_name}!")
        player_achievements = db_get_all_achievements_of_a_player(state, player_name)
        if player_achievements:
            print("")
            print_and_center("You have already got the following achievements in previous games:")
            print_and_center(f"{' '.join(player_achievements)}")

        # Create new save in database
        create_new_save(state, player_name)

        time.sleep(2)
        clear_screen()
        bridge_crash_sound_effect = pygame.mixer.Sound(resource_path('assets/small-rock-break-194553.mp3'))
        bridge_crash_sound_effect.set_volume(state["volume"])
        bridge_crash_sound_effect.play()
        # Message when you first start a new game
        print("You cross the bridge on the second floor to the Applied Computer Science department.", end="")
        print(r"""
         __    ___    __    __   _         __  __  __
        / /`  | |_)  / /\  ( (` | |_|     |_/ |_/ |_/
        \_\_, |_| \ /_/--\ _)_) |_| |     (_) (_) (_)""")
        print("The bridge collapses behind you. You will have to find another way out...")
        time.sleep(6)
        # Start timer
        state["start_time"] = time.time()

    room_functions = { # Collection of the two important functions from each room
        "cloud_room": {"enter_function": cloudroom_enter, "room_commands": cloudroom_commands},
        "computer_lab": {"enter_function": computer_lab_enter, "room_commands": computer_lab_commands},
        "control_room": {"enter_function": controlroom_enter, "room_commands": controlroom_commands},
        "cyber_room": {"enter_function": cyberroom_enter, "room_commands": cyberroom_commands},
        "dragon_room": {"enter_function": dragon_room_enter, "room_commands": dragon_room_commands},
        "riddle_room": {"enter_function": riddleroom_enter, "room_commands": riddleroom_commands},
        "study_landscape": {"enter_function": study_landscape_enter, "room_commands": study_landscape_commands},
        "e_w_corridor": {"enter_function": e_w_corridor_enter, "room_commands": e_w_corridor_commands},
        "lab_corridor": {"enter_function": lab_corridor_enter, "room_commands": lab_corridor_commands},
        "n_s_corridor": {"enter_function": n_s_corridor_enter, "room_commands": n_s_corridor_commands},
        "library": {"enter_function": library_enter, "room_commands": library_commands},
        "roof_garden": {"enter_function": roof_garden_enter, "room_commands": roof_garden_commands},
    }
    room_exits = { # Define exits of all rooms
        "cloud_room": ["lab_corridor"],
        "computer_lab": ["lab_corridor"],
        "control_room": ["e_w_corridor"],
        "cyber_room": ["n_s_corridor"],
        "dragon_room": ["n_s_corridor"],
        "riddle_room": ["n_s_corridor"],
        "study_landscape": ["e_w_corridor", "lab_corridor", "library"],
        "e_w_corridor": ["roof_garden", "control_room", "n_s_corridor", "study_landscape"],
        "lab_corridor": ["computer_lab", "cloud_room", "study_landscape"],
        "n_s_corridor": ["e_w_corridor", "cyber_room", "riddle_room", "dragon_room"],
        "library": ["study_landscape"],
        "roof_garden": ["e_w_corridor"]
    }
    # start game music
    game_music = pygame.mixer.Sound(resource_path('assets/myuu - Stronger Together.mp3'))
    game_music.set_volume(state["volume"])
    game_music.play(loops=-1, fade_ms=3000)

    # print entry banner for the first room
    print("")
    print_room_entry_banner(db_get_current_room(state))

    # Display the enter message of the first room (or the room you are in, when loading a save)
    room_functions[db_get_current_room(state)]["enter_function"](state)

    ###################################################
    # Main game loop
    ###################################################
    while True:

        current_room = db_get_current_room(state)
        # Get command from user
        command = input(Color.blue+"> ").strip().lower()
        print(Color.end)

        # execute admin go
        if command.startswith("admin go "):
            handle_admin_go(command, state, room_functions, room_exits)
            continue

        # Check if the user input is a basic command and execute it
        basic_command_executed = handle_basic_commands(command, state, room_exits)

        if command == "pause":
            quit_flag = pause_menu(state, game_music)
            if quit_flag:
                basic_command_executed = "quit"
            else:
                clear_screen()
                # print entry banner and room entry of curren room
                print_room_entry_banner(db_get_current_room(state))
                continue

        if basic_command_executed == "quit": # Check if quit command
            game_music.stop() #stop music
            return

        # Check if the user input is a command specific to the current room
        room_command_executed = room_functions[current_room]["room_commands"](command, state)

        # If the player should be thrown out of a room the room function can return "go back" which is here converted to the command:
        if type(room_command_executed) == str:
            command = room_command_executed

        # Check for win condition
        if command == "WIN":
            db_update_elapsed_time(state)
            db_set_game_finished(state)
            time.sleep(12)
            db_award_achievement(state, "finish_a_game")
            end_screen(state)
            credits_screen()
            game_music.stop() #stop music
            return
        # Execute going to a different room
        go_executed = handle_go(command, state, room_functions, room_exits)

        # If neither a go command, a room command or a basic command was executed display this:
        if not (go_executed or room_command_executed or basic_command_executed):
            print("Please enter a valid command. Type '?' to get help.")
        print("")

#--------------Definition or variables on start up-------------#
# Set console width if possible
#cmd = 'mode 82,50'
#os.system(cmd)

# create database and connection to it
appdata = os.getenv('LOCALAPPDATA')  # typically C:\Users\username\AppData\Local
db_path = os.path.join(appdata, "EscapeTheNightmare", "saves.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
path = db_path
starting_room = "study_landscape"
state = {
    "db_conn": sqlite3.connect(path),
    "save_id": None,
    "start_time": None,
    "volume": 0.2,
}

# Basic parameters for the database
state["db_conn"].execute("PRAGMA foreign_keys = ON;")
state["db_conn"].execute("PRAGMA journal_mode = WAL;")
# Create tables in the database
init_db(state)

#init sound player
pygame.mixer.init()

clear_screen()
intro_screen(state)

# Switch between main menu and game loop
while True:
    save_id = main_menu(state)
    clear_screen()
    game_loop(save_id)
    clear_screen()

