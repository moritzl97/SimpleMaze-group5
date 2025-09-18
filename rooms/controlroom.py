def control_room(state):
    print("You enter the control room.")
    print("You see a keycard on the floor")
    print("The door you just came through is now closed.")


    # Step 1: Pick up the keycard
    while True:
        command_take_keycard = "take card"
        action = input(f"What do you do? (type '{command_take_keycard}' to pick up the keycard): ").lower()
        if action == command_take_keycard:
            print("You picked up the keycard.")
            has_keycard = True
            break
        else:
            print("You need to take the keycard to continue.")

    # Step 2: Arrange cables
    correct = ["red", "blue", "green", "yellow"]

    attempts = 0

    while True:
        action = input("Type 'arrange cables' to try putting the cables in order: ").lower()
        if action == "arrange cables":
            order = input("Enter the cable colors in order, separated by commas (e.g. red,blue,green,yellow): ")
            cables = [color.strip() for color in order.lower().split(",")]

            if cables == correct:
                print("Correct! You connected the cables properly.")
                print("You get a USB stick to move on.")
                return "corridor"
            else:
                attempts += 1
                print("Wrong order. Try again.")
                if attempts >= 3:
                    print("Hint: Look at the diagram on the wall.")
        else:
            print("You need to arrange the cables to continue.")