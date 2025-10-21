# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

def project_room_3_enter(state):
    # --- Check if the player has the key to enter ---
    if not state["completed"]["project_room_3"]:
        if "key" not in state["inventory"]:
            print("\n🚪 The door to Project Room 3 is locked.")
            print("You jiggle the handle. It's no use.")
            print("🔐 You need a key. Perhaps it's hidden elsewhere in the school?")
            return False
        else:
            print("\n🗝️ You insert the brass key into the lock and turn it with a satisfying click.")
            print("The door creaks open to reveal a bright and lively workspace.")

    # --- Room entry description ---
    print("\n🏗️ You enter Project Room 3.")
    print("Several tables are pushed together, covered in papers, laptops, and half-eaten snacks.")
    print("A group of students is finishing a project while chatting and laughing.")
    return True

# --- Command handlers ---
def handle_look(state):
    """Describe the room and give clues."""
    print("\nYou scan the room.")
    print("The walls are covered in sticky notes, whiteboards are full of pseudocode and diagrams.")
    if not state["completed"]["project_room_3"]:
        print("Near the snack table, one student holds up a fruit and says:")
        print("'You know what they say... which fruit keeps the doctor away?'")
        print("Another grins and says, 'Classic. We always bring them during hackathons.'")
        print("Seems like a riddle. Maybe it's part of the challenge?")
    else:
        print("The students have left. Only empty wrappers and a few notebooks remain.")

def handle_help(state):
    if not state["completed"]["project_room_3"]:
        print("- answer <fruit>      : Solve the riddle about the fruit.")

def handle_answer(answer, state):
    """Handle the fruit riddle."""
    if state["completed"]["project_room_3"]:
        print("✅ You've already completed this room.")
        return True
    normalized = answer.strip().lower()
    if normalized in ["apple", "an apple", "apples"]:
        print("✅ Correct! One of the students claps. 'Of course. Apples every time.'")
        state["completed"]["project_room_3"] = True
        print("\n🎉 CONGRATULATIONS!")
        print("You've explored the project room.")
        return True
    else:
        print("❌ The student shrugs. 'Nope, that one's not it. Think classic.'")
        print("You decide to step out and think it over.")
        return "go back"

def project_room_3_commands(command, state):
    if command == "look around":
        handle_look(state)
        return True
    elif command == "?" or command == "help":
        handle_help(state)
        return True
    elif command.startswith("answer "):
        guess = command[7:].strip()
        result = handle_answer(guess, state)
        return result
    return False
