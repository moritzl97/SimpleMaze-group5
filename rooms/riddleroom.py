# --- Adventure Game: Riddle Room ---

def enterRiddleroom(state):
    inventory = []
    magnet_taken = False
    game_running = True

    def show_status():
        print("\n--- Current Status ---")
        print("Location: Classroom 1.07")
        print("Inventory:", inventory)
        print("---------------------\n")

    def classroom_menu():
        print("You are inside Classroom 1.07.")
        if not magnet_taken:
            print("A shiny magnet is in a locked glass case. The teacher is watching you.")
        else:
            print("The glass case is empty now. The teacher nods approvingly.")

        options = ["Look around"]
        if not magnet_taken and "challenge_solved" in inventory:
            options.append("Take magnet")
        options.append("Check inventory")
        options.append("Quit")

        print("Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Choose an option (number): ").strip()
        return choice, options

    def look_around():
        if not magnet_taken:
            print("The magnet is in a locked glass case. The chalkboard reads: 'Solve the challenge to unlock it.'")
        else:
            print("The classroom is empty except for the usual lab equipment.")

    def take(item):
        nonlocal magnet_taken
        if item == "magnet":
            if "challenge_solved" in inventory:
                inventory.append("magnet")
                magnet_taken = True
                print("You take the magnet and add it to your inventory.")
            else:
                print("The magnet is locked. Solve the challenge first.")

    import random

    def complex_challenge():
        if "challenge_solved" in inventory:
            print("The teacher nods. You already solved the challenge here.")
            return True

        print("\n--- Complex Challenge ---")

        # --- STEP 1: RIDDLE WITH OPTIONS ---
        riddles = [
            {
                "question": "I am taken from a mine, locked in a wooden case, never released, yet almost everyone uses me. What am I?",
                "answer": "pencil",
                "options": ["coal", "diamond", "pencil", "charcoal"],
                "hint": "It's commonly used in schools."
            },
            {
                "question": "The more of this you take, the more you leave behind. What is it?",
                "answer": "footsteps",
                "options": ["time", "footsteps", "memories", "water"],
                "hint": "They make a sound when you walk."
            },
            {
                "question": "What has keys but can't open locks?",
                "answer": "piano",
                "options": ["keyboard", "piano", "map", "safe"],
                "hint": "You can play music on it."
            }
        ]

        selected_riddle = random.choice(riddles)
        print(f'The teacher asks: "{selected_riddle["question"]}"')

        for i, option in enumerate(selected_riddle["options"], start=1):
            print(f"{i}. {option.capitalize()}")

        attempts = 2
        riddle_answer = ""
        while attempts > 0:
            riddle_answer = input("Your answer (or type 'hint'): ").strip().lower()
            if riddle_answer == "hint":
                print(f"HINT: {selected_riddle['hint']}")
                continue
            if riddle_answer == selected_riddle["answer"]:
                print("Correct! Well done.")
                break
            else:
                attempts -= 1
                print(f"Wrong. Attempts left: {attempts}")
        else:
            print("The teacher shakes his head. Come back when you're wiser.")
            return False

        # --- STEP 2: LOGIC PUZZLE ---
        print("\n--- Logic Puzzle ---")
        print("Three friends (Alice, Bob, and Carol) are sitting in a row.")
        print("Bob is not at either end. Carol is not next to Alice. Who is sitting in the middle?")
        logic_answer = input("Your answer: ").strip().lower()

        if logic_answer != "bob":
            print("Incorrect. The puzzle resets.")
            return False
        else:
            print("✅ Correct! You're sharp.")

        # --- STEP 3: MATH PROBLEM ---
        print("\n--- Math Challenge ---")
        print("Solve this to get part of the final code: (12 * 7) + 5")
        try:
            math_answer = int(input("Your answer: ").strip())
        except ValueError:
            print("Invalid input. Challenge failed.")
            return False

        if math_answer != 89:
            print("Incorrect. The teacher shakes his head. Challenge failed.")
            return False
        else:
            print("Math solved!")

        # --- STEP 4: FINAL CODE ---
        print("\n--- Final Code ---")
        print("Combine: [first letter of riddle answer] + [logic answer length] + [math answer]")
        expected_code = (
                selected_riddle["answer"][0]
                + str(len(logic_answer))
                + str(math_answer)
        )

        final_input = input("Enter the code: ").strip().lower()

        if final_input == expected_code:
            print("🔓 The glass case clicks open. You may now take the magnet!")
            inventory.append("challenge_solved")
            state["visited"]["riddleroom"] = True
            return True
        else:
            print("Incorrect code. The challenge remains unsolved.")
            return False

    # --- Start Game ---
    print("Welcome to the Adventure Game!")
    print("Goal: Solve the multi-step challenge in the room to take the magnet.\n")

    # Trigger complex challenge immediately at start
    complex_challenge()

    while game_running:
        show_status()
        choice, options = classroom_menu()
        try:
            selected_option = options[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Try again.")
            continue

        if selected_option == "Look around":
            look_around()
        elif selected_option == "Take magnet":
            take("magnet")
        elif selected_option == "Check inventory":
            print("Inventory:", inventory)
        elif selected_option == "Quit":
            print("Thanks for playing!")
            game_running = False
            return "corridor"
        else:
            print("Invalid choice.")

