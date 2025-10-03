# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

def classroom_2015_enter(state):
    print("\n🏫 You step into Classroom 2.015.")
    print("The classroom is filled with students. A teacher turns toward you, visibly annoyed.")
    print("The door creaks shut behind you. Everyone is looking at you; it's completely silent.")
    return True

# --- handler functions ---
def handle_look(state):
    print("\nYou take a careful look around the room.")
    print("At the front is a whiteboard completely filled with formulas.")
    print("Desks with students are arranged in neat rows, though one chair is oddly turned toward the window.")
    print("On the teacher's desk, a calculator is lying in a strange position on the table.")
    if not state["visited"]["classroom_2015"]:
        print("The teacher says, you are late! And he asks you a question:")
        print("\"What is 7 * 6?\"")
    else:
        print("The teacher sighs: You again? You already solved the challenge.")
        if "key" not in state["inventory"]:
            print("On the desk, beneath the calculator, something metallic glints. It looks like a small key.")
        else:
            print("The desk is empty. You've already taken the key.")

def handle_help(state):
    if not state["visited"]["classroom_2015"]:
        print("- answer <number>     : Attempt to solve the math question.")
    if state["visited"]["classroom_2015"] and "key" not in state["inventory"]:
        print("- take key            : Pick up the key once it's revealed.")

def handle_take(item, state):
    if item == "key":
        if not state["visited"]["classroom2015"]:
            print("❌ There's no key visible yet. Maybe solving the puzzle will reveal more.")
        elif "key" in state["inventory"]:
            print("You already have the key in your backpack.")
        else:
            print("🔑 You lift the calculator from te desk and find a small brass key underneath.")
            print("You take it and tuck it safely into your backpack.")
            state["inventory"].append("key")
    else:
        print(f"There is no '{item}' here to take.")

def handle_answer(answer, state):
    if state["visited"]["classroom2015"]:
        print("✅ You've already solved this challenge.")
    elif answer == "42":
        print("✅ Correct! The teacher invites you to the desk.")
        state["visited"]["classroom2015"] = True
        print("Suddenly you see something on the desk.")
    else:
        print("❌ Incorrect. The teacher opens the door of the classroom.")
        print("You are gently guided back into the corridor.")
        return "go back"

def classroom_2015_commands(command, state):
    if command == "look around":
        handle_look(state)
        return True
    elif command == "?" or command == "help":
        handle_help(state)
        return True
    elif command.startswith("take "):
        item = command[5:].strip()
        handle_take(item, state)
        return True
    elif command.startswith("answer "):
        answer = command[7:].strip()
        result = handle_answer(answer, state)
        if result:
            return result
        else:
            return True
