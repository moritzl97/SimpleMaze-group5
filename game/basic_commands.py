# All commands that are available in all rooms are stored here

import sys
import time

def display_time(state):
    elapsed = int(time.time() - state["time"])
    print(f"Elapsed time: {elapsed} seconds")

def handle_go(command, state, room_functions):
    if command.startswith("go "):
        destination_input = command[3:]
        if destination_input == "back":
            destination_room = state["previous_room"][:]
        else:
            destination_room = destination_input.replace(" ", "_")

        current_room = state["current_room"]

        if destination_room in state["exits"].get(current_room, []):

            print(f"You walk toward the door to {destination_room}.")
            entry_allowed = room_functions[destination_room]["enter_function"](state)

            if entry_allowed:
                state["previous_room"] = state["current_room"]
                state["current_room"] = destination_room
        else:
            print(f"❌ You can't go to '{destination_input}' from here.")
        return True
    else:
        return False

def handle_admin_go(command, state, room_functions):
    destination_room = command[9:]

    current_room = state["current_room"]

    print(f"You walk toward the door to {destination_room}.")
    entry_allowed = room_functions[destination_room]["enter_function"](state)

    if entry_allowed:
        state["previous_room"] = state["current_room"]
        state["current_room"] = destination_room

    else:
        print(f"❌'{destination_room}' doesn't exists.")
    return True

def handle_help():
    #Show help message with available commands.
    print("\nAvailable commands:")
    print("- look around         : See what’s in the lobby.")
    print("- go <room>           : Go to the entered room.")
    print("- go back             : Return to the room you came from.")
    print("- ?                   : Show this help message.")
    print("- pause               : Pause the game")
    print("- quit                : Quit the game.")

def handle_pause():
    pass

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

    current_position = player_positions.get(current_room)

    # Insert X in the map for the player position the other stuff \033[93m is just to print the X in a specific color
    current_map = floor_map[:current_position] + "\033[93mX\033[00m" + floor_map[current_position + 1:]
    print(current_map)
    print(f"Possible exits: {', '.join(state['exits'][current_room])}")

def handle_basic_commands(command, state):
    if command == "quit":
        handle_quit()
    elif command == "pause":
        handle_pause()
        return True
    elif command == "map":
        show_map(state)
        return True
    elif command == "help" or command == "?":
        handle_help()
        return True
    elif command == "inventory" or command == "inv":
        show_inventory(state)
        return True
    return False