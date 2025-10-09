# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

# All commands that are available in all rooms are stored here
import sys
import time
import math
from game.utils import clear_screen


def handle_pause(state):
    if not state["paused"]:
        state["paused"] = True
        state["elapsed_time"] = time.time() - state["start_time"]
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
        print("You can type 'time', 'resume', or 'quit'.")

        while state["paused"]:
            command = input("> ").strip().lower()

            if command == "time":
                display_time(state)

            elif command == "resume":
                handle_resume(state)
                break

            elif command == "quit":
                handle_quit()

            else:
                print("Game is paused. Only available commands: time, resume and quit.")
    else:
        print("Game is already paused.")



def handle_resume(state):
    if state["paused"]:
        state["paused"] = False
        state["start_time"] = time.time() - state["elapsed_time"]
        print("Game resumed.")
    else:
        print("Game is not paused.")


def display_time(state):
    if state["paused"]:
        elapsed = state["elapsed_time"]
    else:
        elapsed = time.time() - state["start_time"]

    print(f"Elapsed time: {int(elapsed)} seconds")


def handle_go(command, state, room_functions):
    if command.startswith("go "):
        destination_room = command[3:]
        if destination_room == "back":
            destination_room = state["previous_room"][:]
        else:
            destination_room = destination_room.replace(" ", "_").replace("-", "_")
        destination_room_display_name = destination_room.replace("_", " ").title()

        current_room = state["current_room"]

        if destination_room in state["exits"].get(current_room, []):
            clear_screen()
            print(f"You walk toward the door to {destination_room_display_name}.")
            destination_name_len = len(destination_room_display_name)
            banner = """
        .-=~=-.                                                                 .-=~=-.
        (__  _)-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-(__  _)
        ( _ __)                                                                 ( _ __)
        (__  _)                                                                 (__  _)
        ( _ __)                                                                 ( _ __)
        (_ ___)-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-=-._.-(_ ___)
        `-._.-'                                                                 `-._.-'
        """
            print(banner[:314-int(destination_name_len/2)]+destination_room_display_name+banner[314+math.ceil(destination_name_len/2):])

            entry_allowed = room_functions[destination_room]["enter_function"](state)

            if entry_allowed:
                state["previous_room"] = state["current_room"]
                state["current_room"] = destination_room
        else:
            print(f"❌ You can't go to '{destination_room_display_name}' from here.")
        return True
    else:
        return False

def handle_admin_go(command, state, room_functions):
    destination_room = command[9:].replace(" ", "_").replace("-", "_")

    current_room = state["current_room"]

    print(f"You walk toward the door to {destination_room}.")
    entry_allowed = room_functions[destination_room]["enter_function"](state)

    if entry_allowed:
        state["previous_room"] = state["current_room"]
        state["current_room"] = destination_room

    else:
        print(f"You can't enter right now.")
    return True

def handle_help():
    #Show help message with available commands.
    print("\nAvailable commands:")
    print("- look around         : See what’s in the lobby.")
    print("- go <room>           : Go to the entered room.")
    print("- go back             : Return to the room you came from.")
    print("- map                 : Shows the map and all exits.")
    print("- inventory           : Shows all items in your inventory.")
    print("- ?                   : Show this help message.")
    print("- pause               : Pause the game")
    print("- quit                : Quit the game.")
    print("- status              : Show the progress of the game")


def handle_quit():
    print(f"👋 You come to the conclusion that this isn't for you."
          "You turn around and leave the building.")
    sys.exit()

def show_inventory(state):
    #list items in inventory
    if state["inventory"]:
        print("You are carrying:")
        for item in state["inventory"]:
            print(f" - {item}")
    else:
        print("You are not carrying anything.")

def show_progress(state):
    visited_rooms = sum(1 for v in state["visited"].values() if v)
    total_rooms = len(state["visited"])
    percentage = (visited_rooms / total_rooms) * 100
    nickname = state.get("player_name", "Player")

    print(f"\nProgress for {nickname}: {visited_rooms}/{total_rooms} rooms visited ({percentage:.1f}%)")
    print("-" * 70)

    # 🏆 Update scoreboard
    state["scoreboard"][nickname] = percentage

    # 📝 Display sorted scoreboard
    print("🏆 Scoreboard:")
    sorted_scores = sorted(state["scoreboard"].items(), key=lambda x: x[1], reverse=True)
    for rank, (name, score) in enumerate(sorted_scores, start=1):
        print(f"{rank}. {name:<15} {score:.1f}%")
    print("-" * 70)


def show_map(state):
    current_room = state["current_room"]
    floor_map = """
+---------+------------+-------------+--------+----------+----------+---------+----------+
|         |            |             |        |          |          |  Cyber  |          |
|         |  Computer  |             |        |  Class   |          |  Room   |  Riddle  |
|         |  Lab       |   Study     |        |  2015    |          +----+-##-+  Room    |
|  Cloud  |            |   Landscape |        |          |          |    #    |          |
|  Room   |            |             +----##--+-------##-+-------##-+----+    #          |
|         +-------##---+             #            E-W-Corridor           #  N |          |
|         # Lab Cor    #            +--------##-+-##-+-##-+-##-+-##-+-##-+  S +----------+
|         +------------+-#-+-#-+    |           |    |    |    |    |    |    |          |
|         |            |   |   |    |  Control  |    |    |    |    |    |  C |  Dragon  |
|         |            |   |PR3|    |  Room     |    |    |    |    |    |  o #  Room    |
+---------+            +---+---+-##-+-----------+----+----+----+----+----+  r |          |
                               |    |                                    +----+----------+
    """

    player_positions = {
        "cloudroom": 734,
        "computerlab": 382,
        "controlroom": 771,
        "cyberroom": 259,
        "dragon_room": 1086,
        "riddleroom": 539,
        "classroom_2015": 417,
        "project_room_3": 849,
        "study_landscape": 577,
        "e_w_corridor": 591,
        "lab_corridor": 659,
        "n_s_corridor": 441,
    }

    current_position = player_positions.get(current_room, False)

    # Insert X in the map for the player position the other stuff \033[93m is just to print the X in a specific color
    if current_position:
        current_map = floor_map[:current_position] + "\033[93mX\033[00m" + floor_map[current_position + 1:]
    else:
        current_map = floor_map

    print(current_map)
    print(f"Possible exits: {', '.join(state['exits'][current_room]).replace("_"," ").title()}")

def handle_basic_commands(command, state):
    if command == "quit":
        handle_quit()
    elif command == "pause":
        handle_pause(state)
        return True
    elif command == "map":
        show_map(state)
        return True
    elif command == "status":
        show_progress(state)
        return True
    elif command == "help" or command == "?":
        handle_help()
        return True
    elif command == "inventory" or command == "inv":
        show_inventory(state)
        return True

    elif command == "time":
        display_time(state)
        return True

    elif command == "resume":
        handle_resume(state)
        return True


    return False