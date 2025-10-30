import random
import time
from rooms.Cyberroom_db_utils import (
    cr_mark_panel_solved,
    cr_is_panel_solved,
    cr_are_all_panels_solved,
    cr_set_terminal_unlocked,
    cr_is_terminal_unlocked,
)
from game.db_utils import db_is_item_in_inventory, db_add_item_to_inventory, db_award_achievement
from game.utils import Color

def _sync_cyberroom_from_db(state):
    if "cyberroom" not in state or "panels" not in state["cyberroom"]:
        return
    # panels
    for pid in ("1", "2", "3"):
        if pid in state["cyberroom"]["panels"]:
            if cr_is_panel_solved(state, pid):
                state["cyberroom"]["panels"][pid]["solved"] = True
    # terminal
    state["cyberroom"]["code_unlocked"] = cr_is_terminal_unlocked(state)




#Main entry point for the CyberRoom
def cyberroom_enter(state):
    # Check if the room has already been completed (the player solved everything before)
    if state["completed"].get("cyberroom", False):
        print("You try to enter the CyberRoom again, but the terminal hums quietly, everything here is already solved.")
        return False

    # If the player has visited before, keep their previous progress
    if "cyberroom" in state and "panels" in state["cyberroom"]:
        _sync_cyberroom_from_db(state)
        panels = state["cyberroom"]["panels"]
        # Separate solved and unsolved panels for display
        solved = [k for k, v in panels.items() if v["solved"]]
        unsolved = [k for k, v in panels.items() if not v["solved"]]

        # Print progress based on what’s already solved
        if solved:
            print("You step back into the Cyberroom. Some panels are still glowing looks like you've already solved a few.")
            print(f"Solved panels: {', '.join(solved)}. Remaining: {', '.join(unsolved)}.\n")
        else:
            print("You step back into the CyberRoom. The glowing panels flicker softly — your previous progress remains.")
        _sync_cyberroom_from_db(state)
        return True

    # First time entering the room
    print("You step into the CyberRoom.")
    print("In front of you, a big terminal blocks the exit.")
    print("The screen flashes: Access denied, security code required.")
    print("The walls are tall screens filled with cascading green code, but most of it is glitching, stuttering, and breaking apart.")
    print("Next to it, three panels flicker with mathematical problems.\n")

    # Helper function to generate random math problems
    def random_problem():
        while True:
            # Randomly choose between 3 expression patterns for variety
            pattern = random.choice([1, 2, 3])

            # Pattern 1: basic 3-number expression
            if pattern == 1:
                a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
                op1, op2 = random.choice(["+", "-", "*"]), random.choice(["+", "-", "*"])
                expr = f"{a} {op1} {b} {op2} {c}"

            # Pattern 2: includes parentheses
            elif pattern == 2:
                a, b, c = random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)
                op1 = random.choice(["+", "-", "*"])
                op2 = random.choice(["+", "-", "*", "/"])
                expr = f"({a} {op1} {b}) {op2} {c}"

            # Pattern 3: two parenthetical expressions combined
            else:
                a, b, c, d = [random.randint(1, 10) for _ in range(4)]
                op1 = random.choice(["+", "-", "*"])
                op2 = random.choice(["+", "-", "*", "/"])
                expr = f"({a} {op1} {b}) {op2} ({c} + {d})"

            # Try to evaluate the expression and only accept positive integer results
            try:
                result = eval(expr)
                if isinstance(result, (int, float)) and result > 0 and float(result).is_integer():
                    # Return both the expression and its correct answer
                    return {"question": expr, "answer": str(int(result))}
            except ZeroDivisionError:
                # Ignore any division by zero and generate a new problem
                continue

    # Create 3 math problems for the 3 panels
    problems = [random_problem() for _ in range(3)]

    # Combine answers into a single numeric code (as a string)
    code = "".join([p["answer"].replace(".", "") for p in problems])

    # Store all CyberRoom state data in the game state dictionary
    state["cyberroom"] = {
        "panels": {
            "1": {"question": problems[0]["question"], "answer": problems[0]["answer"], "solved": False},
            "2": {"question": problems[1]["question"], "answer": problems[1]["answer"], "solved": False},
            "3": {"question": problems[2]["question"], "answer": problems[2]["answer"], "solved": False},
        },
        "code_unlocked": False,
        "correct_code": code
    }

    # Return True so the game knows the player entered successfully
    return True


# Handles the player typing “look around”
def handle_look(state):
    print("You see three panels: panel 1, panel 2, panel 3.")
    panels = state["cyberroom"]["panels"]
    solved = [k for k, v in panels.items() if v["solved"]]
    unsolved = [k for k, v in panels.items() if not v["solved"]]

    # Display which panels are solved or unsolved
    if unsolved:
        print(f"Unsolved panels: {', '.join(unsolved)}")
    if solved:
        print(f"Solved panels: {', '.join(solved)}")

    # Hints depending on player progress
    if all(v["solved"] for v in panels.values()) and not state["cyberroom"]["code_unlocked"]:
        print("The terminal waits for a code maybe the numbers from the panels?")
    if state["cyberroom"]["code_unlocked"] and "?_key" not in state["inventory"]:
        print("The terminal is open. A glowing key hovers inside.")
    if "?_key" in state["inventory"]:
        print("You already took the key.")
    print("Possible exit: n s corridor")


# Handles solving one panel
def handle_panel(panel, state):
    panels = state["cyberroom"]["panels"]

    # Validate the chosen panel number
    if panel not in panels:
        print("That panel does not exist.")
        return

    # Skip if already solved
    if panels[panel]["solved"]:
        print(f"Panel {panel} is already solved.")
        print(f"Solved: {panels[panel]['question']} = {Color.red}{panels[panel]['answer']}\033[0m")
        return

    # Ask the player to solve the math problem
    q = panels[panel]["question"]
    ans = input(f"Solve: {q} = ")

    # Check correctness and mark panel solved if correct
    if ans.strip() == panels[panel]["answer"]:
        print(f"Correct! Panel {panel} solved.")
        panels[panel]["solved"] = True
        cr_mark_panel_solved(state, panel)
    else:
        print("Wrong. Try again.")

        # Achievement
        state["cyberroom"].setdefault("attempts", {"1": 0, "2": 0, "3": 0})
        state["cyberroom"].setdefault("gave_go_back_to_school", False)
        state["cyberroom"]["attempts"][panel] += 1
        if (
                state["cyberroom"]["attempts"][panel] == 2
                and not state["cyberroom"]["gave_go_back_to_school"]
        ):
            print("\033[33mAchievement unlocked:\033[0m \033[1m\"Go back to school📓\"\033[0m")
            db_award_achievement(state, "schoolnerd")
            state["cyberroom"]["gave_go_back_to_school"] = True


# Handles entering the final terminal code
def handle_code(command, state):
    # If the code has already been entered, don’t repeat
    if state["cyberroom"]["code_unlocked"]:
        print("The terminal is already unlocked, the key glows inside.")
        return

    if not cr_are_all_panels_solved(state):
        print("You feel the terminal rejecting you, all panels must be solved first.")
        return

    # Require a second argument (the code number)
    parts = command.split(" ")
    if len(parts) < 2:
        print("Enter a code, e.g. 'code 123'")
        return

    guess = parts[1]

    # Compare the guess with the correct code stored earlier
    if guess == state["cyberroom"]["correct_code"]:
        matrix_rain(rows=16, cols=48, delay=0.04)
        print("Terminal unlocked! A key appears inside the terminal.")
        state["cyberroom"]["code_unlocked"] = True
        cr_set_terminal_unlocked(state, True)

    else:
        print("Wrong code. The terminal beeps angrily.")
        print("Maybe align the digits you got from the panels?")


# Handles taking the Cyber key after unlocking
def handle_take_key(state):
    if state["cyberroom"]["code_unlocked"] and "?_key" not in state["inventory"]:
        print("You take the key and put it in your backpack.")
        db_add_item_to_inventory(state, "?_key")
        # Mark the CyberRoom as completed
        state["completed"]["cyberroom"] = True
        # Add the key to inventory
        state["inventory"].append("?_key")
    elif "?_key" in state["inventory"]:
        print("You already have the key.")
    else:
        print("There is no key yet.")


# Displays the list of possible commands for the player
def handle_help():
    print("\nCyberroom commands:")
    print("look around   = Look around the room")
    print("panel <1/2/3> = Try solving a math panel")
    print("code <......>    = Enter the terminal code")
    print("take key      = Take the cyber key if unlocked")
    print("help or ?     = Show this help again")

def matrix_rain(rows=16, cols=48, delay=0.06):
    GREEN = "\033[32m"
    RESET = "\033[0m"
    for _ in range(rows):
        line = "".join(random.choice("01") for _ in range(cols))
        print(f"{GREEN}{line}{RESET}")
        time.sleep(delay)


# Command router: connects player input to the right handler
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
    elif command == "take key":
        handle_take_key(state)
        return True
    elif command in ["help", "?"]:
        handle_help()
        return True
    return False