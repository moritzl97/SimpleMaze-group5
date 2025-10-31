# =============================================================================
# Room: CyberRoom
# Description:
#   This room presents the player with math puzzles that unlock a terminal.
#   A ghost NPC (Casper) interacts with the player, offering dialogue and a moral
#   choice at the end (release or trap the ghost). The room progress is saved
#   entirely in the database
# =============================================================================

import random
import time

# Import helper functions for saving/loading CyberRoom-specific progress
from rooms.Cyberroom_db_utils import (
    cr_mark_panel_solved,
    cr_is_panel_solved,
    cr_are_all_panels_solved,
    cr_set_terminal_unlocked,
    cr_is_terminal_unlocked,
)

# Import general database utilities for inventory, achievements, etc.
from game.db_utils import (
    db_is_item_in_inventory,
    db_add_item_to_inventory,
    db_award_achievement,
    db_mark_room_completed,
)

# ANSI color codes for styled text (e.g., red answer color)
from game.utils import Color


# -----------------------------------------------------------------------------
# Entry function - triggered when player enters the CyberRoom
# -----------------------------------------------------------------------------
def cyberroom_enter(state):
    # If player has already been here, show progress based on DB data
    if "cyberroom" in state and "panels" in state["cyberroom"]:
        solved = [pid for pid in ("1", "2", "3") if cr_is_panel_solved(state, pid)]
        unsolved = [pid for pid in ("1", "2", "3") if not cr_is_panel_solved(state, pid)]

        # Show which panels were solved before
        if solved:
            print(
                "You step back into the Cyberroom. Some panels are still glowing; looks like you've already solved a few.")
            print(f"Solved panels: {', '.join(solved)}. Remaining: {', '.join(unsolved)}.\n")
        else:
            print(
                "You step back into the CyberRoom. The glowing panels flicker softly — your previous progress remains.")
        return True

    # --- First time entering the room ---
    print("You step into the CyberRoom.")
    print("In front of you, a big terminal blocks the exit.")
    print("The screen flashes: Access denied, security code required.")
    print(
        "The walls are tall screens filled with cascading green code, but most of it is glitching, stuttering, and breaking apart.")
    print("Next to it, three panels flicker with mathematical problems.\n")

    # Internal function to generate random math expressions for panels
    def random_problem():
        while True:
            pattern = random.choice([1, 2, 3])
            # Each pattern defines a slightly different math problem layout
            if pattern == 1:
                a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
                op1, op2 = random.choice(["+", "-", "*"]), random.choice(["+", "-", "*"])
                expr = f"{a} {op1} {b} {op2} {c}"
            elif pattern == 2:
                a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
                op1 = random.choice(["+", "-", "*"])
                op2 = random.choice(["+", "-", "*", "/"])
                expr = f"({a} {op1} {b}) {op2} {c}"
            else:
                a, b, c, d = [random.randint(1, 10) for _ in range(4)]
                op1 = random.choice(["+", "-", "*"])
                op2 = random.choice(["+", "-", "*", "/"])
                expr = f"({a} {op1} {b}) {op2} ({c} + {d})"

            # Evaluate result and ensure it’s a positive integer
            try:
                result = eval(expr)
                if isinstance(result, (int, float)) and result > 0 and float(result).is_integer():
                    return {"question": expr, "answer": str(int(result))}
            except ZeroDivisionError:
                continue  # Skip invalid problems

    # Generate 3 math problems for the 3 panels
    problems = [random_problem() for _ in range(3)]
    code = "".join([p["answer"].replace(".", "") for p in problems])  # Combine answers to form the final unlock code

    # Store minimal in-memory data (no DB duplication)
    state["cyberroom"] = {
        "panels": {
            "1": {"question": problems[0]["question"], "answer": problems[0]["answer"]},
            "2": {"question": problems[1]["question"], "answer": problems[1]["answer"]},
            "3": {"question": problems[2]["question"], "answer": problems[2]["answer"]},
        },
        "correct_code": code,
        "attempts": {"1": 0, "2": 0, "3": 0},
        "gave_go_back_to_school": False,
        # The ghost NPC’s dialogue and state
        "ghost": {
            "met": False,
            "commented_after_panels": False,
            "commented_after_unlock": False,
            "choice_made": False
        },
    }
    return True


# -----------------------------------------------------------------------------
# Handles 'look around' command
# Shows room description, ghost intro, and progress hints
# -----------------------------------------------------------------------------
def handle_look(state):
    ghost = state["cyberroom"].setdefault("ghost", {"met": False, "commented_after_panels": False,
                                                    "commented_after_unlock": False})

    # Ghost intro scene (printed once)
    if not ghost["met"]:
        print("""
        ⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣦⠀
        ⠀⠀⠀⠀⣰⣿⡟⢻⣿⡟⢻⣧
        ⠀⠀⠀⣰⣿⣿⣇⣸⣿⣇⣸⣿
        ⠀⠀⣴⣿⣿⣿⣿⠟⢻⣿⣿⣿
        ⣠⣾⣿⣿⣿⣿⣿⣤⣼⣿⣿⠇
        ⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠀
        ⠀⠀⠈⠿⠿⠋⠙⢿⣿⡿⠁⠀
        """)
        time.sleep(2)
        print("A soft chill sweeps through the room… pixels swirl into a figure.")
        print("Oh! A new student? It’s been ages.")
        print("I’m Casper. I got… stuck here. Don’t worry, I’m just watching.")
        time.sleep(3)
        ghost["met"] = True

    print("\nYou see three panels: panel 1, panel 2, panel 3.")

    # Retrieve solved/unsolved panels from database
    solved = [pid for pid in ("1", "2", "3") if cr_is_panel_solved(state, pid)]
    unsolved = [pid for pid in ("1", "2", "3") if not cr_is_panel_solved(state, pid)]

    # Display progress feedback
    if unsolved:
        print(f"Unsolved panels: {', '.join(unsolved)}")
    if solved:
        print(f"Solved panels: {', '.join(solved)}")

    term_open = cr_is_terminal_unlocked(state)
    has_key = db_is_item_in_inventory(state, "?_key")

    # Dialogue after all panels are solved
    if all(cr_is_panel_solved(state, p) for p in ("1", "2", "3")) and not term_open:
        print("The terminal waits for a code maybe the numbers from the panels?")
        if ghost["met"] and not ghost["commented_after_panels"]:
            print("You… actually did it. I never got this far.")
            ghost["commented_after_panels"] = True

    # After terminal is unlocked, ghost foreshadows the choice
    if term_open and not has_key:
        print("The terminal is open. A glowing key hovers inside.")
        if ghost["met"] and not ghost["commented_after_unlock"]:
            print("That door… it’s my way out. If you let me go.")
            print("You decide what happens to me.")
            ghost["commented_after_unlock"] = True

    if has_key:
        print("You already took the key.")

    print("Possible exit: n s corridor")


# -----------------------------------------------------------------------------
# Handles solving a math panel
# -----------------------------------------------------------------------------
def handle_panel(panel, state):
    panels = state["cyberroom"]["panels"]

    # Validate panel number
    if panel not in ("1", "2", "3"):
        print("That panel does not exist.")
        return

    # Skip if already solved (DB truth)
    if cr_is_panel_solved(state, panel):
        print(f"Panel {panel} is already solved.")
        print(f"Solved: {panels[panel]['question']} = {Color.red}{panels[panel]['answer']}{Color.end}")
        return

    # Ask player to solve
    q = panels[panel]["question"]
    ans = input(f"Solve: {q} = ")

    # Correct answer
    if ans.strip() == panels[panel]["answer"]:
        print("Correct! Panel {0} solved.".format(panel))
        cr_mark_panel_solved(state, panel)
        if cr_are_all_panels_solved(state):
            print("All panels are solved! Maybe you should try interacting with the terminal...")

    else:
        print("Wrong. Try again.")

        state["cyberroom"].setdefault("attempts", {"1": 0, "2": 0, "3": 0})
        state["cyberroom"].setdefault("gave_go_back_to_school", False)
        state["cyberroom"]["attempts"][panel] += 1

        if state["cyberroom"]["attempts"][panel] == 2 and not state["cyberroom"]["gave_go_back_to_school"]:
            db_award_achievement(state, "schoolnerd")
            state["cyberroom"]["gave_go_back_to_school"] = True

        ghost = state["cyberroom"].get("ghost", {})
        if ghost.get("met", False):
            jokes = [
                "It’s okay. I failed that one… a lot.",
                "Math.exe has stopped responding.",
                "Deep breath. Try the order… the correct one.",
                "Do you even know what math is?"
                  ]
            print(f"{random.choice(jokes)}")


# -----------------------------------------------------------------------------
# Handles entering the final terminal code
# -----------------------------------------------------------------------------
def handle_code(command, state):
    # Prevent re-entry if already unlocked
    if cr_is_terminal_unlocked(state):
        print("The terminal is already unlocked, the key glows inside.")
        return

    # Require all panels solved first
    if not cr_are_all_panels_solved(state):
        print("You feel the terminal rejecting you, all panels must be solved first.")
        return

    # Ensure the player entered a number after "code"
    parts = command.split(" ")
    if len(parts) < 2:
        print("Enter a code, e.g. 'code 123'")
        return

    guess = parts[1]

    # If correct, unlock terminal and trigger ghost dialogue
    if guess == state["cyberroom"]["correct_code"]:
        matrix_rain(rows=16, cols=48, delay=0.08)
        print("Terminal unlocked!")
        cr_set_terminal_unlocked(state, True)

        ghost = state["cyberroom"]["ghost"]
        if ghost["met"] and not ghost["commented_after_unlock"]:
            print("That’s it… The door’s open. I can finally leave.......if you let me.")
            print("Type 'release ghost' to free me, or 'lock ghost' to keep me here.")
            ghost["commented_after_unlock"] = True
        else:
            # If ghost was never met, show key immediately
            print("The ?_key appears inside the terminal, humming softly.")
    else:
        print("Wrong code. The terminal beeps angrily.")
        print("Maybe align the digits you got from the panels?")


# -----------------------------------------------------------------------------
# Ghost choice: Release or lock after unlocking the terminal
# -----------------------------------------------------------------------------
def handle_release_ghost(state):
    if not cr_is_terminal_unlocked(state):
        print("The terminal is still locked.")
        return
    if db_is_item_in_inventory(state, "?_key"):
        print("Too late. The moment has passed; the room is silent.")
        return

    print("You’d really let me go? After all this time… thank you.")
    matrix_rain(rows=8, cols=50, delay=0.08)
    print("The ghost dissolves into the flowing code and fades from sight.")
    db_award_achievement(state, "ghost_release")

    # Mark choice made and spawn key
    state["cyberroom"]["ghost"]["choice_made"] = True
    print("The ?_mark key glows inside!")


def handle_lock_ghost(state):
    if not cr_is_terminal_unlocked(state):
        print("The terminal is still locked.")
        return
    if db_is_item_in_inventory(state, "?_key"):
        print("Too late. The room has already reset to silence.")
        return

    print("…You’re serious. Just like the others.")
    print("The lights flicker green for a moment, then steady again.")
    matrix_rain(rows=4, cols=50, delay=0.08)
    db_award_achievement(state, "ghost_lock")

    #  choice made and spawn key
    state["cyberroom"]["ghost"]["choice_made"] = True
    print("The ?_mark key glows inside!")


# -----------------------------------------------------------------------------
# Handles taking the key (adds to DB inventory)
# -----------------------------------------------------------------------------
def handle_take_key(state):
    term_open = cr_is_terminal_unlocked(state)
    has_key = db_is_item_in_inventory(state, "?_key")

    if term_open and not has_key:
        print("You take the key and put it in your backpack.")
        db_add_item_to_inventory(state, "?_key")
        db_mark_room_completed(state, "Cyberroom")


        if state["cyberroom"].get("ghost", {}).get("met"):
            print("Whatever happens… thanks for trying.")
    elif has_key:
        print("You already have the key.")
    else:
        print("There is no key yet.")


# -----------------------------------------------------------------------------
# Displays all commands available in the CyberRoom
# -----------------------------------------------------------------------------
def handle_help():
    print("\nCyberroom commands:")
    print("- look around         : Look around the room")
    print("- panel <1/2/3>       : Try solving a math panel")
    print("- code <......>       : Enter the terminal code")
    print("- take key            : Take the key if unlocked")
    print("- release ghost       : Free the classmate ghost (after unlock, before key)")
    print("- lock ghost          : Keep the ghost trapped (after unlock, before key)")


# -----------------------------------------------------------------------------
# Visual effect for terminal animation (Matrix-like rain)
# -----------------------------------------------------------------------------
def matrix_rain(rows=16, cols=48, delay=0.06):
    GREEN = "\033[32m"
    RESET = "\033[0m"
    for _ in range(rows):
        line = "".join(random.choice("01") for _ in range(cols))
        print(f"{GREEN}{line}{RESET}")
        time.sleep(delay)


# -----------------------------------------------------------------------------
# Command router - links user input to the correct handler
# -----------------------------------------------------------------------------
def cyberroom_commands(command, state):
    if command == "look around":
        handle_look(state)
        return True
    elif command.startswith("panel "):
        panel = command.split(" ")[1]
        handle_panel(panel, state)
        return True
    elif command.startswith("code "):
        handle_code(command, state)
        return True
    elif command == "release ghost":
        handle_release_ghost(state)
        return True
    elif command == "lock ghost":
        handle_lock_ghost(state)
        return True
    elif command == "take key":
        handle_take_key(state)
        return True
    elif command in ["help", "?"]:
        handle_help()
        return True
    return False