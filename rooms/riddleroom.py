# --- Adventure Game: Complex Challenge ---

inventory = []
visited = True  # Start directly in the room
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
    global magnet_taken
    if item == "magnet":
        if "challenge_solved" in inventory:
            inventory.append("magnet")
            magnet_taken = True
            print("You take the magnet and add it to your inventory.")
        else:
            print("The magnet is locked. Solve the challenge first.")


def complex_challenge():
    if "challenge_solved" in inventory:
        print("The teacher nods. You already solved the challenge here.")
        return True

    print("\n--- Challenge ---")

    # Step 1: Riddle
    print(
        'The teacher asks: "I am taken from a mine, locked in a wooden case, never released, yet almost everyone uses me. What am I?"')
    riddle_answer = input("Your answer: ").strip().lower()

    if riddle_answer != "pencil":
        print("Wrong! The teacher shakes his head. Try again later.")
        return False
    else:
        print("Correct! Now for the math part.")

    # Step 2: Simple math problem
    print("Solve this to get part of the code: What is 12 * 7 + 5 ?")
    try:
        math_answer = int(input("Your answer: ").strip())
    except ValueError:
        print("Invalid input. Challenge failed.")
        return False

    if math_answer != 89:  # 12*7 + 5 = 84 + 5 = 89
        print("Incorrect. The teacher shakes his head. Challenge failed.")
        return False
    else:
        print("Correct! Now combine your answers for the final code.")

    # Step 3: Code generation
    # Let's say code is first letter of riddle + math answer
    code = riddle_answer[0] + str(math_answer)  # e.g., 'p89'
    print("Enter the final code to unlock the magnet (format: first letter of riddle + math answer)")
    final_input = input("Code: ").strip().lower()

    if final_input == code:
        print("Correct! The glass case clicks open. You may now take the magnet.")
        inventory.append("challenge_solved")
        return True
    else:
        print("Incorrect code. The challenge remains unsolved.")
        return False


# --- Main Game Loop ---
print("Welcome to the Adventure Game!")
print("Goal: Solve the multi-step challenge in the room to take the magnet.\n")

# Trigger complex challenge immediately at start
complex_challenge()

while game_running:
    show_status()
    choice, options = classroom_menu()
    selected_option = options[int(choice) - 1]

    if selected_option == "Look around":
        look_around()
    elif selected_option == "Take magnet":
        take("magnet")
    elif selected_option == "Check inventory":
        print("Inventory:", inventory)
    elif selected_option == "Quit":
        print("Thanks for playing!")
        game_running = False
    else:
        print("Invalid choice.")
