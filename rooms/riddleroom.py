# --- Adventure Game: Riddle Room ---
import random

def riddleroom_enter(state):
    print("Welcome to the Adventure Game!")
    print("Goal: Solve the multi-step challenge in the room to take the magnet.\n")
    state["riddleroom"]["magnet_taken"] = False #TODO only set state if it is not set yet
    return True

def riddleroom_commands(command, state):
    challenge_solved = complex_challenge(state) # TODO Maybe don't just start the challenge but let the player start it by e.g. talking to the teacher
    if challenge_solved:
        print("You are inside Classroom 1.07.")
        if not state["riddleroom"]["magnet_taken"]:
            print("A shiny magnet is in a locked glass case. The teacher is watching you.")
        else:
            print("The glass case is empty now. The teacher nods approvingly.")

        if command == "look around": #TODO add return True to all commands
            look_around(state)
        elif command == "take magnet" and not state["riddleroom"]["magnet_taken"] and "challenge_solved" in state["inventory"]:
            take("magnet", state)
    else:
        print(f"you failed the challenge, you can come back later")
        return "go back"

def look_around(state):
    if not state["riddleroom"]["magnet_taken"]:
        print("The magnet is in a locked glass case. The chalkboard reads: 'Solve the challenge to unlock it.'")
    else:
        print("The classroom is empty except for the usual lab equipment.")

def take(item, state):

    if item == "magnet":
        if "challenge_solved" in state["inventory"]:
            state["inventory"].append("magnet")
            state["riddleroom"]["magnet_taken"] = True
            print("You take the magnet and add it to your inventory.") #TODO add the state["completed"]["riddleroom"] = True here instead of below
        else:
            print("The magnet is locked. Solve the challenge first.")



def complex_challenge(state):
    if "challenge_solved" in state["inventory"]: # TODO challenge_solved shouldn't be an item added to the inventory, but a boolean flag in the state
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

    # --- STEP 2: LOGIC PUZZLE --- #TODO Maybe split the puzzles such that the player has to start each round (you can look at the cyberroom for an example, Tieme did it there with the panels)
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
        state["inventory"].append("challenge_solved")
        state["completed"]["riddleroom"] = True
        return True
    else:
        print("Incorrect code. The challenge remains unsolved.")
        return False



