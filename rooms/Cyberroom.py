import random


def cyberroom_enter(state):
    #completed
    if state["completed"].get("cyberroom", False):
        print("You try to enter the CyberRoom again, but the terminal hums quietly, everything here is already solved.")
        return False

    #keeps progress
    if "cyberroom" in state and "panels" in state["cyberroom"]:
        panels = state["cyberroom"]["panels"]
        solved = [k for k, v in panels.items() if v["solved"]]
        unsolved = [k for k, v in panels.items() if not v["solved"]]

        if solved:
            print("You step back into the Cyberroom. Some panels are still glowing looks like you've already solved a few.")
            print(f"Solved panels: {', '.join(solved)}. Remaining: {', '.join(unsolved)}.\n")
        else:
            print("You step back into the CyberRoom. The glowing panels flicker softly — your previous progress remains.")
        return True

    #first time in the room
    print("You step into the CyberRoom.")
    print("In front of you, a big terminal blocks the exit.")
    print("The screen flashes: Access denied, security code required.")
    print("The walls are tall screens filled with cascading green code, but most of it is glitching, stuttering, and breaking apart.")
    print("Next to it, three panels flicker with mathematical problems.\n")

    def random_problem():
        while True:
            pattern = random.choice([1, 2, 3])

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

            try:
                result = eval(expr)
                if isinstance(result, (int, float)) and result > 0 and float(result).is_integer():
                    return {"question": expr, "answer": str(int(result))}
            except ZeroDivisionError:
                continue

    problems = [random_problem() for _ in range(3)]

    code = "".join([p["answer"].replace(".", "") for p in problems])

    state["cyberroom"] = {
        "panels": {
            "1": {"question": problems[0]["question"], "answer": problems[0]["answer"], "solved": False},
            "2": {"question": problems[1]["question"], "answer": problems[1]["answer"], "solved": False},
            "3": {"question": problems[2]["question"], "answer": problems[2]["answer"], "solved": False},
        },
        "code_unlocked": False,
        "correct_code": code
    }

    return True


def handle_look(state):
    print("You see three panels: panel 1, panel 2, panel 3.")
    panels = state["cyberroom"]["panels"]
    solved = [k for k, v in panels.items() if v["solved"]]
    unsolved = [k for k, v in panels.items() if not v["solved"]]

    if unsolved:
        print(f"Unsolved panels: {', '.join(unsolved)}")
    if solved:
        print(f"Solved panels: {', '.join(solved)}")

    if all(v["solved"] for v in panels.values()) and not state["cyberroom"]["code_unlocked"]:
        print("The terminal waits for a code maybe the numbers from the panels?")
    if state["cyberroom"]["code_unlocked"] and "cyber_key" not in state["inventory"]:
        print("The terminal is open. A glowing key hovers inside.")
    if "cyber_key" in state["inventory"]:
        print("You already took the key.")
    print("Possible exit: n s corridor")


def handle_panel(panel, state):
    panels = state["cyberroom"]["panels"]

    if panel not in panels:
        print("That panel does not exist.")
        return

    if panels[panel]["solved"]:
        print(f"Panel {panel} is already solved.")
        return

    q = panels[panel]["question"]
    ans = input(f"Solve: {q} = ")

    if ans.strip() == panels[panel]["answer"]:
        print(f"Correct! Panel {panel} solved.")
        panels[panel]["solved"] = True
    else:
        print("Wrong. Try again.")


def handle_code(command, state):
    if state["cyberroom"]["code_unlocked"]:
        print("The terminal is already unlocked, the key glows inside.")
        return

    parts = command.split(" ")
    if len(parts) < 2:
        print("Enter a code, e.g. 'code 123'")
        return

    guess = parts[1]

    if guess == state["cyberroom"]["correct_code"]:
        print("Terminal unlocked! A key appears inside the terminal.")
        state["cyberroom"]["code_unlocked"] = True
    else:
        print("Wrong code. The terminal beeps angrily.")
        print("Maybe align the digits you got from the panels?")


def handle_take_key(state):
    if state["cyberroom"]["code_unlocked"] and "cyber_key" not in state["inventory"]:
        print("You take the key and put it in your backpack.")
        state["completed"]["cyberroom"] = True
        state["inventory"].append("cyber_key")
    elif "cyber_key" in state["inventory"]:
        print("You already have the key.")
    else:
        print("There is no key yet.")


def handle_help():
    print("\nCyberroom commands:")
    print("look around   = Look around the room")
    print("panel <1/2/3> = Try solving a math panel")
    print("code <......>    = Enter the terminal code")
    print("take key      = Take the cyber key if unlocked")
    print("help or ?     = Show this help again")


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
