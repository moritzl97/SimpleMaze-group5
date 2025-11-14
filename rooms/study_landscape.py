# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================
from game.db_utils import *
from game.utils import *

def study_landscape_enter(state):
    print("\nYou step into the study landscape.")
    print("You see soft chairs and tables to work and chat with fellow students. You hear the quiet hum of a coffee machine.")
    print("It feels like a place to work but also to pause and catch your breath.")
    print("However, you feel a ominous presence in one corner.")
    if not db_get_flag(state, "tutorial_finished") and not db_is_item_in_inventory(state, "python_tutorial"):
        print("You know there is a roof window in the library. Maybe you could try escape from there? Type 'go library' to enter the library.")
    elif db_is_item_in_inventory(state, "python_tutorial"):
        print("The librarian waits for you delivery. Type 'talk librarian' to talk to her.")


    state["coffee_drank"] = 0
    return True

def handle_look(state):
    print("You take a slow look around.")
    print("In the corner of the room you see something ominous. You see a pentagram inside a Summoning Circle, carefully drawn with chalk, on the floor.")
    print("Weirdly nobody else seams to notice the Summoning Circle.")
    print("On one desk you see a librarian frantically searching through a pile of books.")
    if not db_get_flag(state, "tutorial_finished"):
        print("Because you are new here, maybe you could get some guidance from her. You should talk to her with 'talk librarian'.")

def handle_look_summoning_circle(state):
    print(r"""
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⢤⠤⢤⠤⣤⢤⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡤⠴⠖⠚⠛⠉⠁⠀⡀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣄⣤⣀⣀⣀⣀⡀⠈⠉⠉⠛⠓⠲⠦⠤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠴⠚⠋⠉⣀⣠⣤⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣤⣀⡀⠈⠙⠓⠶⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠞⠋⠁⣀⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⡀⠈⠙⠳⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠋⠁⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠈⠛⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠞⠋⢀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠈⠙⠳⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠞⠋⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠙⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⢁⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣷⣤⡀⠈⠛⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⢀⣠⣾⣉⣛⣛⠛⣛⣛⣋⣉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠋⠉⠀⢀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣦⣤⣤⣤⣤⣤⣀⣀⣀⠀⠈⠉⠙⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠡⣦⣤⡌⢹⣿⣿⣿⣿⣦⡀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⢀⣴⣿⣿⣿⣯⠉⢉⣍⣉⣍⣍⠙⢸⣿⣿⣿⣿⣿⣿⡿⠟⠋⠉⢀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣄⡀⠈⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣶⣤⠉⣡⣾⣿⣿⣿⣿⣿⣿⣦⡀⠀⠙⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⢀⣴⣿⣿⣿⣿⣿⣿⣇⢸⣿⣿⣿⣿⣧⢈⣿⣿⣿⠿⠋⠁⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠉⠻⢿⣿⣿⣿⣿⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠙⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠁⣠⣿⣿⣿⣿⣿⣿⣿⠉⡼⢸⣿⣿⣿⣿⣿⣾⠿⠋⠀⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠘⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠃⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⡿⠛⠁⢀⡐⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⢹⣇⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣠⣶⣿⣇⠀⠀⣈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣤⡆⠀⣼⣿⣷⣦⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠈⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣠⣾⣿⣿⣿⣿⡄⠀⢌⢳⣄⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣡⣴⢋⡽⠀⢰⣿⣿⣿⣿⣿⣦⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠻⣄⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⣰⠃⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⣠⣾⣿⣿⣿⣿⣿⣿⣷⠀⠈⢳⡌⢿⣦⣈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣠⣾⠏⣁⡾⠁⢀⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠹⣆⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣼⠃⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠻⣦⡉⠻⣷⣦⡈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣡⡶⠟⢋⣡⣾⠏⡀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠸⣆⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⣼⠃⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣀⠀⡙⢿⣄⣤⡘⠻⢷⣄⡙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⣡⡾⠛⠛⣠⣶⣼⠟⣡⠞⠁⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠘⣆⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⣸⠇⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⣆⠹⣆⠙⢿⣷⡄⣄⠙⠛⢶⣌⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣩⣵⠟⢉⢠⣶⣾⡿⠋⣠⡾⠃⣴⢃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠹⡄⠀⠀⠀⠀
        ⠀⠀⠀⣰⠏⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢹⣧⠘⢷⣄⠙⠿⣿⣦⣤⡀⠹⠷⣦⣈⠻⢿⣿⣿⣿⣿⣿⣿⣿⠿⢋⣠⡾⠟⠉⣰⣿⣿⠟⠉⣠⣾⠟⢁⣼⠇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⢻⡀⠀⠀⠀
        ⠀⠀⢀⡟⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⣧⡀⠻⣿⣦⡈⠻⢿⣷⣦⢠⡈⠛⢷⣄⡉⠻⣿⣿⠟⣉⣤⣶⡿⠟⢁⣿⣿⣿⠟⢁⣴⣾⡿⠋⣠⣾⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠈⣇⠀⠀⠀
        ⠀⠀⣸⠁⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠸⣿⣿⣄⠙⢿⣿⣦⡈⠹⣿⣾⣷⠰⣆⠹⣿⣷⣇⠀⣾⣿⣿⡟⣰⣶⣿⣿⠏⢠⣴⣿⣿⡟⠁⣴⣿⣿⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⢸⡆⠀⠀
        ⠀⠀⡏⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢻⣿⣿⣦⠀⢿⣿⣿⣦⡘⠻⣿⣶⣷⣀⣀⣹⣿⣿⣦⠈⠀⠀⣿⣿⣿⢓⣴⣿⣿⣿⡏⢀⣾⣿⣿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⢷⠀⠀
        ⠀⢸⠁⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⣿⣿⣿⣧⠀⢻⣿⣿⣿⣿⠛⣿⣶⣿⣿⠃⠿⠟⠛⠀⣿⣦⣌⠛⢻⣿⣿⣿⣿⡏⢀⣿⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⡆⠀
        ⠀⡌⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢹⣿⣿⣿⣧⠀⣿⣿⣿⣧⣷⡟⢿⡿⣿⣤⣴⣶⣶⣴⣿⣿⠿⣵⣮⡏⠛⣿⣿⠀⣾⣿⣿⣿⠃⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠈⣇⠀
        ⢀⠇⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢿⣿⣿⡿⢓⢨⣿⣿⣻⣿⣿⣜⣷⡜⣿⣿⣿⣿⣿⣿⣿⢠⣿⣿⣿⢳⣬⡁⠸⣿⣿⣿⡏⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⢻⠀
        ⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡾⢿⣳⣾⣿⢹⣿⣿⡘⠟⣿⣿⣿⣷⡈⢿⣿⣿⠟⣿⣿⣿⣿⣿⡿⢸⣿⣇⢠⣍⡙⠿⢦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠘⡇
        ⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢋⣥⣼⣿⣿⠃⣸⣿⣿⣷⡀⠸⣿⣿⣿⣿⡈⣿⣇⣾⣿⣿⣿⣿⣿⢃⣾⣿⣿⠀⢿⣷⣄⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⡅
        ⠸⠀⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⣡⣶⣿⣿⣏⣿⡏⣰⣿⣿⡿⣿⣿⣄⠈⠻⣿⣿⣇⠈⣼⣿⣿⡿⠛⣹⣷⣿⣿⣿⣿⣧⡈⠛⣻⣿⣷⣄⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⠀⡅
        ⠸⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢁⣴⣾⣿⣿⡿⡟⠋⣨⣿⣿⣿⣿⣧⠻⣿⣿⣷⣄⠘⢿⣿⡄⣿⣿⠋⣠⣾⣿⣿⣿⣿⣿⣿⣿⣷⣀⡈⠛⠿⣿⣿⣦⣈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⡄
        ⢸⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢉⣴⣾⡿⠿⠛⠉⣁⣠⣴⣿⣿⠿⢿⣿⣿⣿⣦⡌⠛⠿⣿⣷⡈⣿⣿⣿⡇⣼⣿⣿⣿⠿⢿⣿⣿⣿⡿⣿⣿⣿⣶⣤⣀⠉⠛⠿⢷⣦⡈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⠀⠀⡄
        ⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣠⡶⠛⢉⣠⣤⣶⣾⣿⣿⣿⡿⠋⢁⠀⠈⣿⣿⣿⡀⠀⣴⠶⣄⢹⣧⢸⣿⣿⣷⣿⠟⢉⣤⠀⡿⢿⣿⡿⠀⠈⠻⣿⣿⣿⣿⣿⣷⣦⣄⡈⠙⢷⣄⠙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
        ⢸⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢉⣠⠾⠋⣠⣴⣾⣿⠿⠿⠿⠛⠛⣉⣤⡶⢿⡇⠀⢹⣿⣿⣇⠀⠉⠀⣸⡦⢿⣾⣿⣿⣿⢥⣄⡀⣹⠋⢣⣾⣿⠃⠀⢿⣦⣌⣉⡛⠛⠛⠛⠛⠻⠷⣦⣀⠙⢷⣄⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
        ⢸⡀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⢸⣿⣿⣿⣿⣿⣿⣿⠟⠋⣠⣶⠟⢃⣠⡾⠟⣉⣠⣤⣴⣶⣶⣿⡿⢿⡿⢡⡟⢠⡀⠀⢿⣿⣿⣧⣄⣂⣐⠛⢻⣿⣿⣿⠃⠂⠈⠉⣡⣴⣿⣿⠃⠀⣴⡌⢿⡟⢿⣿⢿⣿⣿⣿⣿⣿⣮⣝⢷⣄⠙⢷⣦⡌⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀
        ⠸⡇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠈⣿⣿⣿⣿⡿⠛⢁⣴⡾⠛⢁⣴⣾⣿⣶⠿⡿⣻⠟⣡⠟⣱⠏⠁⢊⣴⣿⣴⣿⣇⠀⡈⢻⣿⣿⣿⣟⣩⣿⣿⣿⣿⣿⣿⣯⣉⣻⣿⣿⡿⢁⡴⢠⣿⣿⣦⡙⡈⠻⣄⠻⣞⠻⣏⠻⣿⡙⢿⡻⣦⣀⠙⠻⣷⣄⠉⠻⣿⣿⣿⣿⣿⣿⠃⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
        ⠀⣧⠀⢻⣿⣿⣿⠛⣟⣛⡛⢿⣿⣿⣿⡇⠀⢻⣿⠿⡉⠀⠚⠉⠡⠔⣚⣉⣉⣉⣋⣀⣤⣋⣉⣼⣯⣾⣷⣶⣿⣿⣿⣿⣿⣿⣿⡄⢷⣀⠉⣿⣿⣿⡟⣹⣿⣿⣿⣿⡏⢹⣿⣿⡿⠋⣰⣾⠃⣾⣿⣿⣿⣿⣿⣶⣬⣷⣌⣠⣌⣳⣌⡙⣦⡁⠘⣿⡀⡀⠀⠉⠛⠂⠀⠙⠿⣿⣿⡏⠀⢸⣿⣿⡟⠛⠛⠻⢿⣿⣿⣿⣿⡟⠀⠀⠀⠀
        ⠀⢿⡀⠘⣿⣿⣿⠘⠿⠻⠇⣼⣿⣿⣿⣿⠀⠀⣡⣈⡉⣉⣙⣚⣋⣉⠉⢉⠉⢉⣉⣉⢉⡉⡋⠉⡉⠉⠙⠉⠙⠉⠋⠛⠛⠛⢻⣿⡈⣛⠀⢛⣛⠛⠉⢙⠛⠛⠛⠛⡋⠀⠙⠛⠛⠀⢻⠋⠘⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠓⠳⠶⠿⠲⠷⠶⠌⢻⡇⠀⣿⣿⣿⡇⠿⠿⠿⣼⣿⣿⣿⣿⠇⠀⢀⠀⠀
        ⠀⠈⡇⠀⢿⣿⣿⣷⣿⣿⡀⣿⣿⣿⣿⣿⣇⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣾⢻⣿⣿⡟⢿⣿⣿⣿⣿⡟⢀⣾⣿⡟⢀⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡟⠀⣸⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⡿⠀⠀⡇⠀⠀
        ⠀⠀⢿⡀⠘⣿⣿⣿⣿⢠⡇⣿⣿⣿⣿⣿⣿⡄⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⣷⠘⣿⣿⣧⠸⣿⣿⣿⣿⠇⣾⣿⣿⠃⣼⠇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢠⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⣿⣿⠇⠀⡸⠁⠀⠀
        ⠀⠀⠀⣷⠀⢹⣿⣿⣿⠘⣇⢹⣿⣿⣿⣿⣿⣿⡄⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣇⠹⣿⢿⣧⣿⣿⣿⣿⣾⣿⢿⠇⣰⡟⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⢀⣿⣿⣿⣿⣿⣿⣿⣇⣼⣿⣿⣿⡟⠀⢠⠇⠀⠀⠀
        ⠀⠀⠀⠸⣇⠀⢻⣿⣿⣦⠹⡎⣿⣿⣿⣿⣿⣿⣿⡄⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⢻⡄⢹⡟⣿⣿⣿⣿⣿⡿⢡⣟⣰⣿⢤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⡞⠀⠀⠀⠀
        ⠀⠀⠀⠀⢻⡄⠀⢿⣿⣿⣇⠀⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⠀⣇⠈⢻⣿⣿⡏⠀⣸⠏⣼⠇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⡼⠁⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⢻⡄⠈⢿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⡷⠈⠛⠚⠛⣉⣛⣋⠁⢼⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⣼⠃⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⢻⡄⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⢷⡤⢦⣭⣉⣉⣥⡿⣶⡾⢣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⡼⠃⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠹⡄⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠈⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⣧⠘⣿⣿⣿⡿⢡⣿⣅⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⢀⡼⠃⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠹⣆⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣄⢻⣿⣿⠀⣿⠁⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⡀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢿⡀⠹⠋⢸⡇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢳⡄⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣷⣄⣀⣾⢁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠁⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢻⣿⣿⠃⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣠⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣆⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠉⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡈⣿⡏⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⢀⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⡀⠈⠉⠛⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣷⠛⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠟⠛⠋⠁⢀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣤⣀⣀⠀⠉⠉⠉⠉⠙⠛⠂⠘⠛⠙⠋⠉⠉⠉⠉⠁⣀⣀⣠⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣤⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⣄⡀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⣀⡴⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⡀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣭⣤⣭⠶⢤⣤⡌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⣀⡴⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⣤⣀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣬⣤⣤⣴⣶⡆⠙⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⢀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠦⣤⣀⠈⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⠁⢀⣠⡤⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠓⠲⢤⣀⡀⠉⠉⠛⠛⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠛⠛⠋⠉⠀⣀⣤⠤⠒⠚⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠒⠒⠦⢤⣤⣀⣀⣀⣀⠈⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠈⢀⣀⣀⣀⣤⣤⠤⠶⠒⠚⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠙⠋⠙⠋⠙⠋⠛⠋⠛⠉⠉⠉⠀⠀⢀⠀⢀⢀⡀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                """)
    time.sleep(3)
    print("You feel drawn to the ominous circle. Black smoke seams to be emitted from it.")
    all_items_in_inventory = db_get_all_items_in_inventory(state)
    required_items  = ["cursed_trophy", "cursed_rose", "cursed_robot_head", "cursed_magnet"]
    found_all_items = all(item in all_items_in_inventory for item in required_items)
    if found_all_items:
        print("You arrange the items around the circle.")
        print("A dark figure forms out of the smoke.")
        print(f"???: {Color.bold+Color.yellow}Good. Without your help I would not be able to return to this world.{Color.end}")
        print("A portal opens up behind the figure. You see your bedroom and disturbingly yourself sleeping in the bed.")
        print(f"???: {Color.bold+Color.yellow}You can go now.{Color.end}")
        print("You step through the portal.")
        db_mark_room_completed(state, "study_landscape")
        return "WIN"
    else:
        print("You hear a deep voice inside your head.")
        print(f"???: {Color.bold+Color.yellow}You can only escape the nightmare if you bring me all of my 4 cursed items.{Color.end}")
        print("The smoke vanishes.")
        if not db_get_flag(state, "tutorial_finished"):
            print("Curiously you see a book 'Python Tutorial' laying near the circle.")
            print("Taking it will skip the Tutorial.")
            db_set_flag(state, "skip_tutorial", True)
        return True

def handle_talk(state):
    if not db_get_flag(state, "tutorial_finished") and db_is_item_in_inventory(state, "python_tutorial"):
        db_remove_item_from_inventory(state, "python_tutorial")
        print("Librarian: Thank you for delivering my book.")
        print("Librarian: Good luck exploring the school. You can check the map by typing 'map' to see where you can go from here.")
        print("Make sure to type '?' in every room to see which commands are available in this specific room.")
        print("Librarian: You can also have my lab permit to access the computer labs.")
        db_add_item_to_inventory(state, "lab_permit")
        db_set_flag(state, "tutorial_finished", True)
    elif db_get_flag(state, "tutorial_finished") and db_is_item_in_inventory(state, "python_tutorial"):
        db_remove_item_from_inventory(state, "python_tutorial")
        print("Librarian: The librarian looks confused. Oh my book wasn't in the library? Thanks anyway.")
        print("Librarian: Here, you can have my lab permit to access the computer labs.")
        db_add_item_to_inventory(state, "lab_permit")
        db_mark_room_completed(state, "library")
        if not db_is_item_in_inventory(state, "rusty_key"):
            print("Also you can have the library key if you still want to enter it.")
            db_add_item_to_inventory(state, "rusty_key")
    elif not db_get_flag(state, "tutorial_finished"):
        print("\nLibrarian: I am missing my Python tutorial book. Can you fetch it for me from the library? Here is the key.")
        print("The librarian hands you an old rusty key.")
        db_add_item_to_inventory(state, "rusty_key")
        print("With the key now you can enter the library with 'go library'.")
    else:
        print("The librarian is engrossed in reading her books. Better not to disturb her.")

def handle_take(state, item):
    if item == "python tutorial" and db_get_flag(state, "skip_tutorial"):
        print("You pick up the book 'Python Tutorial' near the summoning circle.")
        db_add_item_to_inventory(state, "python_tutorial")
        db_set_flag(state, "tutorial_finished", True)
    else:
        print(f"You can not pick up {item}.")

def handle_help(state):
    print("\nStudy Landscape commands:")
    print("- look around         : Get more information about you surrounding.")
    print("- talk <person>       : Talk to someone in the room")
    print("- look summoning circle: Inspect the ominous circle in the corner.")

def study_landscape_commands(command, state):
    if command == "look around":
        handle_look(state)
        return True
    elif command == "look summoning circle":
        outcome = handle_look_summoning_circle(state)
        return outcome
    elif command == "talk librarian":
        handle_talk(state)
        return True
    elif command.startswith("take "):
        item = command[5:]
        handle_take(state, item)
        return True
    elif command == "?" or command == "help":
        handle_help(state)
        return True
    elif command in ["look coffee machine", "take coffee", "use coffee machine", "make coffee", "drink coffee", "get coffee"]:
        print("You approach the coffee machine and get some coffee. You take a sip of the steaming coffee. The rich aroma fuels your mind and warms your soul.")
        state["coffee_drank"] += 1
        if state["coffee_drank"] >= 3:
            print("You feel the caffeine pulsing through your veins. You will not sleep tonight...")
            db_award_achievement(state, "coffee_adict")
        return True
    return False