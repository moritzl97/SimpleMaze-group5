# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================
from game.db_utils import *

def e_w_corridor_enter(state):
    print("\nYou are standing in the school's main corridor.")
    print("You see a long corridor with many doors and glass walls on both side. Behind these door are rooms, waiting to be explored.")
    print("At the end of the corridor a janitor is cleaning the floor.")
    db_mark_room_completed(state, "e_w_corridor")
    return True

def handle_look():
    print("\nYou take a look around.")
    print("Students and teachers are walking in both directions along the corridor. You see several labeled doors.")
    print("The janitor has put up a 'Do not step on the wet floor!' sign.")

def handle_talk(state):
    if db_is_item_in_inventory(state, "beer") and db_is_item_in_inventory(state, "bottle_opener"):
        db_remove_item_from_inventory(state, "beer")
        db_remove_item_from_inventory(state, "bottle_opener")
        db_set_flag(state, "n_s_unlocked", True)
    elif db_is_item_in_inventory(state, "beer"):
        print("Janitor: Bring me something to open the beer and I will let you through.")
        print("Janitor: In the mean time, please don't step on the freshly mopped floor.")
    elif db_is_item_in_inventory(state, "bottle_opener"):
        print("The janitor looks a bit confused what to do with just a bottle opener.")
        print("Janitor: Don't you see I have work to do? Please don't step on the freshly mopped floor.")
    elif not db_get_flag(state, "n_s_unlocked"):
        print("Janitor: Don't you see I have work to do? Please don't step on the freshly mopped floor.")
    else:
        print("Janitor: Thanks again for the beer!")

def handle_help(state):
    print("East West Corridor commands:")
    print("- talk janitor       : Talk to the janitor")

def e_w_corridor_commands(command, state):
    if command == "look around":
        handle_look()
        return True
    elif command == "talk janitor":
        handle_talk(state)
        return True
    return False