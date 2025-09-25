# All commands that are available in all rooms are stored here

import sys

def handle_help(additional_help = None):
    #Show help message with available commands.
    print("\nAvailable commands:")
    if additional_help:
        for item in additional_help:
            print(item)
    print("- look around         : See what’s in the lobby.")
    print("- go 'room'           : Go to the entered room.")
    print("- back                : Return to the room you came from.")
    print("- ?                   : Show this help message.")
    print("- quit                : Quit the game.")

def handle_go(destination, exits_list, state):
    if destination in exits_list:
        print("You leave the study landscape and head back into the corridor.")
        state["previous_room"] = state["current_room"]
        return destination
    else:
        print(f"❌ You can't go to '{destination}' from here.")
        return None



def pause():
    pass

def quit_game():
    print(f"👋 You come to the conclusion that this isn't for you."
          "You turn around and leave the building.")
    sys.exit()

