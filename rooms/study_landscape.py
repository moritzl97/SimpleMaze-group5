# -----------------------------------------------------------------------------
# File: study_landscape.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

def study_landscape_enter(state):
    print("\n🛋️ You step into the study landscape.")
    print("Soft chairs and tables to work and chat with fellow students and a quiet hum of a coffee machine.")
    print("It feels like a place to work but also to pause and catch your breath.")
    return True

def handle_look():
    """Describe the lobby and show exits."""
    print("\nYou take a slow look around.")
    print("There are a few posters on the wall about upcoming student events.")
    print("A group of students is sitting in the corner gazing at a laptop")

def study_landscape_commands(command, state):
    if command == "look around":
        handle_look()
        return True
