

def enterCyberRoom(state):

    if state["visited"]["cyberroom"] == True:
        print("There is nothing left to do here.")
        return "corridor"

    CR = {"inventory": []}
    print("\n💻 You step into the CyberRoom.")
    print("In front you, a big terminal blocks the exit.")
    print("The screen is flashing: Access denied, security code required.")
    print("The walls are tall screens filled with cascading green code, but most of it is glitching, stuttering, and breaking apart")
    print("Next to it, three panels flicker with mathematical problems")

    print("\ncommands:")
    print("look          = Look around the room")
    print("panel <...>   = Try solving panel 1, 2, or 3")
    print("code <123>    = Enter the terminal code (after solving all panels)")
    print("take key      = Take the cyber key if unlocked")
    print("leave         = Exit back to the corridor")
    print("quit          = Quit the game")


    solved_panels = {"1": False, "2": False, "3": False}
    code_unlocked = False
    correct_code = "289"




    while True:
        command = input("\n> ").strip().lower()

        if command == "look":
            print("You see three panels: panel 1, panel 2, panel 3.")
            if all(solved_panels.values()) and not code_unlocked:
                print("The terminal waits for a 3-digit code.")
            if code_unlocked and "cyber_key" not in CR["inventory"]:
                print("The terminal is open. A key glows inside.")
            if "cyber_key" in CR["inventory"]:
                print("You already took the key.")
            print("Possible exit: leave")

        elif command.startswith("panel "):
            panel = command.split(" ")[1]
            if panel == "1" and not solved_panels["1"]:
                ans = input("Solve: -12 + 7 * 2 = ")
                if ans == "2":
                    print("Correct! Panel 1 solved.")
                    solved_panels["1"] = True
                else:
                    print("Wrong. Try again.")
            elif panel == "2" and not solved_panels["2"]:
                ans = input("Solve: (45 / 9) + 3 = ")
                if ans == "8":
                    print("Correct! Panel 2 solved.")
                    solved_panels["2"] = True
                else:
                    print("Wrong. Try again.")
            elif panel == "3" and not solved_panels["3"]:
                ans = input("Solve: 6 * 3 - 9 = ")
                if ans == "9":
                    print("Correct! Panel 3 solved.")
                    solved_panels["3"] = True
                else:
                    print("Wrong. Try again.")
            else:
                print("That panel is already solved or does not exist.")

        elif command.startswith("code "):
            if all(solved_panels.values()):
                guess = command.split(" ")[1]
                if guess == correct_code:
                    print("Terminal unlocked! A key appears inside.")
                    code_unlocked = True
                else:
                    print("Wrong code.")
            else:
                print("You must solve all panels first.")

        elif command == "take key":
            if code_unlocked and "cyber_key" not in CR["inventory"]:
                print("You take the key and put it in your backpack.")
                CR["inventory"].append("cyber_key")
            elif "cyber_key" in CR["inventory"]:
                print("You already have the key.")
                state["visited"]["cyberroom"] = True
            else:
                print("There is no key yet.")

        elif command == "leave":
            print("You leave the CyberRoom and return to the corridor.")
            return "corridor"

        elif command == "quit":
            print("You quit the game.")
            sys.exit()

        else:
            print("Unknown command. Try: look, panel <n>, code <123>, take key, leave, quit.")
