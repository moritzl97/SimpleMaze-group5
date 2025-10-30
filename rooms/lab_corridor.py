# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================
import time

from game.db_utils import *

def lab_corridor_enter(state):
    if not db_is_item_in_inventory(state, "lab_permit"):
        print("The Laboratory Safety Officer watches you closely as you approach.")
        print("Laboratory Safety Officer: Whoa, whoa, whoa. Not so fast. Have you read the lab safety code? I am not sure you know how to behave in the labs. I will only let you through with a lab permit.")
        return False
    else:
        print("The Laboratory Safety Officer inspects the permit closely.")
        print("Laboratory Safety Officer: You have the right paper work. However I will still watch you closely.")
        print("\nYou are standing in the corridor to the computer labs.")
        print("You hear the sound of servers humming from the neighboring rooms.")
        db_mark_room_completed(state, "lab_corridor")
        return True

def handle_look():
    print("\nYou take a look around.")
    print("Students in lab coats pass by. You are excited to learn what you will find in the labs.")
    print("The Laboratory Safety Officer is watching you through the window of the door to the Study Landscape.")
    print("You see a red button with a sign: 'Do not press' ")

def lab_corridor_commands(command, state):
    if command == "look around":
        handle_look()
        return True
    if command == "press button" or command == "press":
        print("Against your better judgement you press the button...")
        time.sleep(5)
        print("You look around.")
        time.sleep(2)
        print("But still nothing happens... Anyway better to back away before somebody catches you.")
        return True
    return False