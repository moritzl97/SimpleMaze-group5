

def cyberroom_enter(state):
    if state["visited"]["cyberroom"]:
        print("There is nothing left to do here.")
        return False

    print("You step into the CyberRoom.")
    print("In front of you, a big terminal blocks the exit.")
    print("The screen flashes: Access denied, security code required.")
    print("The walls are tall screens filled with cascading green code, but most of it is glitching, stuttering, and breaking apart.")
    print("Next to it, three panels flicker with mathematical problems.\n")

    # Room state
    state["cyberroom"] = {
        "solved_panels": {"1": False, "2": False, "3": False},
        "code_unlocked": False,
        "correct_code": "289"
    }

    return True

def handle_look(state):
    print("You see three panels: panel 1, panel 2, panel 3.")
    if all(state["cyberroom"]["solved_panels"].values()) and not state["cyberroom"]["code_unlocked"]:
        print("The terminal waits for a 3-digit code.")
    if state["cyberroom"]["code_unlocked"] and "cyber_key" not in state["inventory"]:
        print("The terminal is open. A key glows inside.")
    if "cyber_key" in state["inventory"]:
        print("You already took the key.")
    print("Possible exit: n s corridor")


def handle_panel(panel, state):
    panels = state["cyberroom"]["solved_panels"]

    if panel == "1" and not panels["1"]:
        ans = input("Solve: -12 + 7 * 2 = ")
        if ans == "2":
            print("Correct! Panel 1 solved.")
            panels["1"] = True
        else:
            print("Wrong. Try again.")
    elif panel == "2" and not panels["2"]:
        ans = input("Solve: (45 / 9) + 3 = ")
        if ans == "8":
            print("Correct! Panel 2 solved.")
            panels["2"] = True
        else:
            print("Wrong. Try again.")
    elif panel == "3" and not panels["3"]:
        ans = input("Solve: 6 * 3 - 9 = ")
        if ans == "9":
            print("Correct! Panel 3 solved.")
            panels["3"] = True
        else:
            print("Wrong. Try again.")
    else:
        print("That panel is already solved or does not exist.")


def handle_code(command, state):
    if all(state["cyberroom"]["solved_panels"].values()):
        guess = command.split(" ")[1]
        if guess == state["cyberroom"]["correct_code"]:
            print("Terminal unlocked! A key appears inside.")
            state["cyberroom"]["code_unlocked"] = True
        else:
            print("Wrong code.")
    else:
        print("You must solve all panels first.")


def handle_take_key(state):
    if state["cyberroom"]["code_unlocked"] and "cyber_key" not in state["inventory"]:
        print("You take the key and put it in your backpack.")
        state["visited"]["cyberroom"] = True
        state["inventory"].append("cyber_key")
    elif "cyber_key" in state["inventory"]:
        print("You already have the key.")
    else:
        print("There is no key yet.")


def handle_help():
    print("\nCyberroom commands:")
    print("look around   = Have a look around")
    print("panel <...>   = Try solving panel 1, 2, or 3")
    print("code <123>    = Enter the terminal code (after solving all panels)")
    print("take key      = Take the cyber key if unlocked")
    print("leave         = Exit the room")


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

    elif command == "?" or command == "help":
        handle_help()
        return True

    # Return False if command is not recognized (lets main handle it)
    return False
