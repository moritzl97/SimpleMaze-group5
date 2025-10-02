# -----------------------------------------------------------------------------
# File: corridor.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

def n_s_corridor_enter(state):
    print("\n🚶 You are standing in the school's main corridor.")
    print("You see a long corridor with many doors and glass walls on both side. Behind these door are rooms, waiting to be explored.")
    return True

def handle_look():
    """Describe the corridor and show where the player can go."""
    print("\nYou take a look around.")
    print("Students and teachers are walking in both directions along the corridor. You see several labeled doors.")

def n_s_corridor_commands(command, state):
    if command == "look around":
        handle_look()
        return True