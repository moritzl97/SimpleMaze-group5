# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

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