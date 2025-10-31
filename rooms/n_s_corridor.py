# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================
from game.db_utils import *

def n_s_corridor_enter(state):
    if not db_get_flag(state, "n_s_unlocked"):
        print("You try to reach the door to the North-South Corridor. However the janitor blocks the way with his mob.")
        print("He grumbles something about you not respecting his work.")
        print("You will have to find something to appease him, so that he will let you through.")
        return False

    print("The north south corridor is much more quiet. You see nobody around.")
    print("Only a few classrooms are located here.")
    db_mark_room_completed(state, "n_s_corridor")
    return True

def handle_look(state):
    print("\nYou take a look around.")
    print("The corridor is empty. What will await you behind the classroom doors?")
    if not db_is_item_in_inventory(state, "empty_soda_can"):
        print("However, you notice a empty soda can on the floor.")

def handle_take(state):
    db_add_item_to_inventory(state, "empty_soda_can")

def handle_help(state):
    print("\nNorth South Corridor commands:")
    print("- look around         : Looks around in the North South corridor")

def n_s_corridor_commands(command, state):
    if command == "look around":
        handle_look(state)
        return True

    elif command in ["help", "?"]:
        handle_help(state)
        return True

    elif not db_is_item_in_inventory(state, "empty_soda_can") and (command == "take soda can" or command == "take can" or command == "take empty can" or command == "take empty soda can"):
        print("You pick up the empty soda can.")
        print("It is exactly what you thought it would be: A empty soda can.")
        print("You are not sure why you picked it up.")
        return True
    return False