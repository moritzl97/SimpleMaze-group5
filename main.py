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
from game.screens import *
from game.db import init_db, create_new_save
from game.utils import *
from game.db_utils import *
import sqlite3

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
        print("\n\n\n")
        print("Enter your name".center(82))
        print("")
        player_name = input(" " * 37)

        clear_screen()
        print("\n\n\n")
        print(f"Welcome to the Nightmare, {player_name}!".center(82))

        # Create new save in database
        create_new_save(state, player_name)

        time.sleep(2)
        clear_screen()

        # Message when you first start a new game
        print("You cross the bridge on the second floor to the Applied Computer Science department.", end="")
        print(r"""
         __    ___    __    __   _         __  __  __
        / /`  | |_)  / /\  ( (` | |_|     |_/ |_/ |_/
        \_\_, |_| \ /_/--\ _)_) |_| |     (_) (_) (_)""")
        print("The bridge collapses behind you. You will have to find another way out...")
        # time.sleep(6) TODO uncomment
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
        "study_landscape": ["e_w_corridor", "lab_corridor", "project_room_3", "library"],
        "e_w_corridor": ["roof_garden", "control_room", "n_s_corridor", "study_landscape"],
        "lab_corridor": ["computer_lab", "cloud_room", "study_landscape"],
        "n_s_corridor": ["e_w_corridor", "cyber_room", "riddle_room", "dragon_room"],
        "library": ["study_landscape"],
        "roof_garden": ["e_w_corridor"]
    }

    # print entry banner for the first room
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

        if basic_command_executed == "quit": # Check if quit command
            return

        # Check if the user input is a command specific to the current room
        room_command_executed = room_functions[current_room]["room_commands"](command, state)

        # If the player should be thrown out of a room the room function can return "go back" which is here converted to the command:
        if type(room_command_executed) == str:
            command = room_command_executed

        # Check for win condition
        if command == "WIN":
            db_update_elapsed_time(state)
            time.sleep(12)
            db_award_achievement(state, "finish_a_game")
            end_screen(state)
            credits_screen()
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
path = "saves.db"
starting_room = "study_landscape"
state = {
    "db_conn": sqlite3.connect(path),
    "save_id": None,
    "start_time": None,
    #TODO remove all the following values from state variable and add them in the db
    "current_room": starting_room,
    "previous_room": starting_room,
    "completed": {
        "roof_garden": False,
        "cloud_room": False,
        "cyber_room": False,
        "dragon_room": False,
        "computer_lab": False,
        "riddle_room": False,
        "control_room": False,
        "e_w_corridor": False,
        "lab_corridor": False,
        "n_s_corridor": False,
        "library": False,
    },
    "entered": {
        "roof_garden": False,
        "cloud_room": False,
        "cyber_room": False,
        "dragon_room": False,
        "computer_lab": False,
        "riddle_room": False,
        "control_room": False,
        "study_landscape": True,
        "e_w_corridor": False,
        "lab_corridor": False,
        "n_s_corridor": False,
        "library": False,
    },
    "inventory": [],
    "paused": False,
    "elapsed_time": 0,
    "player_name": None,
    "skip_tutorial":False,
    "cloud_room": {},
    "cyber_room": {},
    "computer_lab": {},
    "riddle_room": {},
    "control_room": {},
    "roof_garden": {"weather": None, "talked_to_gardener":False, "dice": [], "orchid":{"water": False, "fertilizer": False, "robot": False}},
    "study_landscape": {"coffee_drank":0}
}
# Basic parameters for the database
state["db_conn"].execute("PRAGMA foreign_keys = ON;")
state["db_conn"].execute("PRAGMA journal_mode = WAL;")
# Create tables in the database
init_db(state)

# Switch between main menu and game loop
while True:
    save_id = main_menu(state)
    clear_screen()
    game_loop(save_id)
    clear_screen()

