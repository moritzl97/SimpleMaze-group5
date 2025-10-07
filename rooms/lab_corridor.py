# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

def lab_corridor_enter(state):
    print("\n🚶 You are standing in the corridor to the computer labs.")
    print("You hear the sound of servers humming from the neighboring rooms.")
    return True

def handle_look():
    """Describe the corridor and show where the player can go."""
    print("\nYou take a look around.")
    print("Students in lab coats pass by. You are excited to learn what you will find in the labs.")

def lab_corridor_commands(command, state):
    if command == "look around":
        handle_look()
        return True