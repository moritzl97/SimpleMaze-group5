def control_room(state):
    print("You enter the control room.")
    print("You see a keycard on the floor.")
    print("The door you just came through is now closed.")

    # Step 1: Pick up the keycard
    while True:
        action = input("What do you do? (e.g. 'take card'): ").lower().strip()
        if action in ["take card", "take keycard", "pick up card"]:
            print("You picked up the keycard.")
            state["has_keycard"] = True
            break
        else:
            print("You need to take the keycard to continue.")

    # Step 2: Puzzle with cables (simple questions)
    print("\nNow you must solve the cable puzzle by answering the color mixes:")

    solved_order = []

    # RED cable
    while True:
        answer = input("What color do you get when you mix magenta + yellow? ").lower().strip()
        if answer == "red":
            print("Correct! Connect the red cable.")
            solved_order.append("red")
            break
        else:
            print("Wrong, try again.")

    # BLUE cable
    while True:
        answer = input("What color do you get when you mix cyan + magenta? ").lower().strip()
        if answer == "blue":
            print("Correct! Connect the blue cable.")
            solved_order.append("blue")
            break
        else:
            print("Wrong, try again.")

    # GREEN cable
    while True:
        answer = input("What color do you get when you mix yellow + blue? ").lower().strip()
        if answer == "green":
            print("Correct! Connect the green cable.")
            solved_order.append("green")
            break
        else:
            print("Wrong, try again.")

    # YELLOW cable
    while True:
        answer = input("What color do you get when you mix red + green light? ").lower().strip()
        if answer == "yellow":
            print("Correct! Connect the yellow cable.")
            solved_order.append("yellow")
            break
        else:
            print("Wrong, try again.")

    # Final check
    if solved_order == ["red", "blue", "green", "yellow"]:
        print("\nYou connected all the cables in the correct order!")
        print("You get a USB stick to move on.")
        state["has_usb"] = True
        state["visited"]["controlroom"] = True
        return "corridor"
