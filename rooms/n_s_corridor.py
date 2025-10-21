# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

def n_s_corridor_enter(state):
    print("\n🚶 The north south corridor is much more quiet.")
    print("Only a few classrooms are located here.")
    state["completed"]["n_s_corridor"] = True
    return True

def handle_look():
    """Describe the corridor and show where the player can go."""
    print("\nYou take a look around.")
    print("The corridor is empty. What will await you behind the classroom doors?")

def n_s_corridor_commands(command, state):
    if command == "look around":
        handle_look()
        return True
    return False