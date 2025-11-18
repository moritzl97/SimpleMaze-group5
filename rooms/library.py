# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================
from game.db_utils import *
from rooms.library_db_utils import *

def handle_help(state):
    print("\nLibrary:")
    print("- look around         : Get more information about you surrounding.")
    print("- take <booktitle>    : Take a book")

def library_enter(state):
    if not db_is_item_in_inventory(state, "rusty_key"):
        print("You try to open the door to the library. However it is locked.")
        if not db_get_flag(state, "tutorial_finished"):
            print("You should try to explore the Study Landscape more closely to find the key. \nType 'look around' to get more information about you surroundings.")
        return False
    else:
        print("\nYou step into the library. You smell old paper and dust.")
        if not db_get_flag(state, "tutorial_finished"):
            print("Type 'look around' to get more information about you surroundings.")
        return True

def handle_look(state):
    print("Dim skylight falls through the roof window. However the window is barred behind steel bars. This is definitely not the right way out.")
    book_order = db_get_book_list(state)
    if book_order:
        time.sleep(2)
        print("""
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⠾⢿⣶⡶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⠶⣶⢾⡿⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣿⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⣇⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣇⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⣿⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣤⣤⡤⠶⠶⢿⠀⢿⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢱⡇⢰⣿⣶⢶⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠈⢹⠟⠶⣤⣜⡛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⣛⣛⣛⣿⣿⡿⠿⠿⠛⠛⠛⠛⠛⢻⡄⢹⡾⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠃⠀⠀⠉⠙⠻⢶⣤⣀⡀⠀⣀⣀⣀⣤⣤⣴⡶⠶⠾⠟⠛⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢸⡇⣿⠀⠀⠀⠀⠀
⠀⠀⠀⣴⣾⣇⡀⠀⠀⠀⠀⠀⠀⠉⠻⣟⢻⡋⣿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠇⢸⣧⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠾⣿⣿⢿⣷⣦⣄⡀⠀⠀⠀⠀⣿⠘⡇⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣤⣾⣶⣾⡿⠷⣦⠀⠀⠀⠀
⠀⠀⠀⠀⢸⡟⠻⢿⣿⣾⣟⡷⣦⣀⠀⣿⢠⡏⢸⡇⠀⠀⠀⠀⢀⣀⣀⣤⣤⣤⣶⣶⣾⣿⡿⠿⠿⠛⠛⠉⠉⠀⠀⠀⠀⢿⡀⠀⠀⠀
⠀⠀⠀⣀⣸⡇⠀⠀⠈⠙⠿⣿⣷⣯⣻⣿⣸⣧⣼⣥⣶⣶⣿⣿⡿⠿⠿⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⡇⠀⠀⠀
⠀⠀⠀⣙⣯⣿⣦⣀⠀⠀⠀⠀⠉⠛⢿⡿⠿⠛⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⡇⠀⠀⠀
⢠⡿⣿⣿⣭⣙⡳⣿⣷⣄⡀⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⣤⡿⣶⣶⣦⡄
⣾⢱⠏⣹⠛⠻⠷⣿⣿⣝⢷⣄⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣴⡶⠶⠿⠛⣛⣭⣽⠷⠿⢿⠋⠁
⣿⢼⠀⡟⠀⠀⠀⠀⠈⠉⠻⣯⡻⣦⣀⣿⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⣤⡴⠶⠶⠛⠛⠋⠉⢉⣀⣤⣤⠶⠞⠛⠉⠁⠀⠀⠀⢸⠀⠀
⣿⢺⡀⣷⠀⠀⠀⠀⠀⠀⠀⠈⠙⢷⣽⣟⣠⣤⣴⢶⣶⣿⣛⡛⠉⠉⠀⠀⠀⢀⣀⣤⣴⠶⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀
⠹⣾⣇⣻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠉⠉⠀⠀⠀⠀⠉⣹⠛⣿⠶⣶⠾⠟⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⠷
⠀⠀⢉⣹⡿⠶⢦⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⢰⡏⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣿⡿⢻⠉⠀⠀
⠀⣾⠿⠷⣶⣦⣤⣬⣭⣟⣳⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⢸⡇⢸⡅⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣿⠿⠛⢋⡽⠋⠀⢸⠀⠀⠀
⢠⡏⠀⠀⠀⠀⠀⠈⠉⠉⠉⠛⠛⠛⠻⠿⠷⢶⣤⣀⡀⠀⣧⢸⡇⠀⢹⠀⠀⠀⠀⣀⣠⣴⣾⣿⠿⠛⠉⠀⢀⡼⠋⠀⠀⠀⢸⠀⠀⠀
⠰⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠳⠿⣦⣷⣀⠸⣇⣤⣶⣿⡿⠿⠿⠿⢶⣦⣤⣤⡴⠋⠀⠀⠀⠀⠀⢸⡀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⣠⣾⠿⠁⠀
⠀⠸⣧⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⣠⣾⡿⠋⠀⠀⠀
⠀⠀⠉⠉⠉⠛⠛⠛⣶⣶⣶⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⣰⣿⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠙⠛⠛⠳⠶⠶⢦⣤⣤⣄⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣠⣾⠟⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠛⠛⠛⠿⠶⠶⣶⣤⣤⣤⣀⣀⣻⣾⡟⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        
        
        """)
        time.sleep(1)
        print("On the top shelf of a bookshelf you see three books stacked ontop of each other. From top to bottom the titles are: ",end="")
        print(f"{', '.join(book_order[::-1])}.")
        print("However you are to small and can only reach the book at the bottom.")
    if not db_get_flag(state, "tutorial_finished"):
        print("Try 'take <something>' to pick it up.")

def handle_take(state, item):
    book_order = db_get_book_list(state)
    if book_order:
        if item == book_order[0]:
            if item == "python tutorial":
                print("You add the Python Tutorial to your inventory.")
                if not db_get_flag(state, "tutorial_finished"):
                    print("You can check your inventory by typing 'inventory'.")
                    print("Now you can return to the librarian by typing 'go study landscape' or 'go back'.")
                db_add_item_to_inventory(state, "python_tutorial")
                db_mark_room_completed(state, "library")
                db_remove_next_book(state, item)
                return
            print("You take the bottom bock and lay it to the side. The outer books shift down.")
            db_remove_next_book(state, item)
        elif item in book_order:
            print("You try to stretch, but you can not reach the books higher on the stack.")
            print("Maybe you should try to take the book lower in the stack?")
        else:
            print(f"There is no {item} in the room.")
            print("Type 'take <booktitle> to take a book.'")
    else:
        print("The shelf is already empty.")

def library_commands(command, state):
    if command == "look around":
        handle_look(state)
        return True
    if command.startswith("take"):
        item = command[5:]
        handle_take(state, item)
        return True
    if command == "?" or command == "help":
        handle_help(state)
        return True
    return False

