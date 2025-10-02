# -----------------------------------------------------------------------------
# File: main.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

import time
from rooms import *
from game.basic_commands import handle_basic_commands, handle_go, handle_admin_go
from game.screens import *

title_screen()
# ----------------------------------------------------------------------
# Progress Helper
# ----------------------------------------------------------------------
def show_progress(state):
    visited_rooms = sum(1 for v in state["visited"].values() if v)
    total_rooms = len(state["visited"])
    percentage = (visited_rooms / total_rooms) * 100
    print(f"\n📊 Progress: {visited_rooms}/{total_rooms} rooms visited ({percentage:.1f}%)")
    print("-" * 70)


# ----------------------------------------------------------------------
# Game State
# ----------------------------------------------------------------------
starting_room = "study_landscape"
state = {
    "current_room": starting_room,
    "previous_room": starting_room,
    "exits": {
        "cloudroom": ["lab_corridor"],
        "computerlab": ["lab_corridor"],
        "controlroom": ["e_w_corridor"],
        "cyberroom": ["n_s_corridor"],
        "dragon_room": ["n_s_corridor"],
        "riddleroom": ["n_s_corridor"],
        "classroom_2015": ["e_w_corridor"],
        "project_room_3": ["study_landscape"],
        "study_landscape": ["e_w_corridor","lab_corridor","project_room_3"],
        "e_w_corridor": ["classroom_2015","controlroom", "n_s_corridor","study_landscape"],
        "lab_corridor": ["coputerlab","cloudroom", "study_landscape"],
        "n_s_corridor": ["e_w_corridor","cyberroom", "riddleroom", "dragon_room"],
    },
    "visited": {
        "classroom_2015": False,
        "project_room_3": False,
        "cloudroom": False,
        "cyberroom": False,
        "dragon_room": False,
        "computerlab": False,
        "riddleroom": False,
        "controlroom": False
    },
    "inventory": [],
    "paused": False,
    "start_time": time.time(),
    "elapsed_time": 0,
    "dragon_room": {}
}

room_functions = {
    "cloudroom": {"enter_function": None, "room_commands": None},
    "computerlab": {"enter_function": None, "room_commands": None},
    "controlroom": {"enter_function": None, "room_commands": None},
    "cyberroom": {"enter_function": cyberroom_enter, "room_commands": cyberroom_commands},
    "dragon_room": {"enter_function": dragon_room_enter, "room_commands": dragon_room_commands},
    "riddleroom": {"enter_function": None, "room_commands": None},
    "classroom_2015": {"enter_function": classroom_2015_enter, "room_commands": classroom_2015_commands},
    "project_room_3": {"enter_function": project_room_3_enter, "room_commands": project_room_3_commands},
    "study_landscape": {"enter_function": study_landscape_enter, "room_commands": study_landscape_commands},
    "e_w_corridor": {"enter_function": e_w_corridor_enter, "room_commands": e_w_corridor_commands},
    "lab_corridor": {"enter_function": lab_corridor_enter, "room_commands": lab_corridor_commands},
    "n_s_corridor": {"enter_function": n_s_corridor_enter, "room_commands": n_s_corridor_commands},
}

state["time"] = time.time()

player_name = input("\nWhat is your nickname:  ")
print(f"\nWelcome, {player_name}! Let's start!\n")

# ----------------------------------------------------------------------
# Game Loop
# ----------------------------------------------------------------------
print("****************************************************************************")
print("*                      Welcome to the School Maze!                         *")
print("*        Your goal is to explore all important rooms in the school.        *")
print("*    You may need to solve challenges to collect items and unlock rooms.   *")
print("*               Once you've visited all rooms, you win!                    *")
print("****************************************************************************")

room_functions[state["current_room"]]["enter_function"](state)

while True:
    current_room = state["current_room"]
    command = input("> ")

    if command.startswith("admin go "):
        handle_admin_go(command,state, room_functions)
        continue

    basic_command_executed = handle_basic_commands(command, state)

    room_command_executed = room_functions[current_room]["room_commands"](command, state)

    if type(room_command_executed) == str:
        command = room_command_executed

    go_executed = handle_go(command, state, room_functions)

    if not (go_executed or room_command_executed or basic_command_executed):
        print("Please enter a valid command. Type '?' to get help.")

    # Show progress after each move
    show_progress(state)

    # Win condition
    if all(state["visited"].values()):
        print("\n🎉 Congratulations! You've visited all the rooms and completed the maze! 🎉")
        break
