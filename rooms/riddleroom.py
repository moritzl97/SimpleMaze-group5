# --- Adventure Game: Riddle Room ---
import random
import time

from game.db_utils import *

def riddleroom_enter(state):
    if not db_is_item_in_inventory(state, '?_key'):
        print("You first have to get question mark key to enter the room")
        return False
    else:
        print("Welcome to the Adventure Game!")
        print("Goal: Solve the multi-step challenge in the room to take the magnet.\n")
        return True

def riddleroom_commands(command, state):
    complex_challenge(state)
    if db_is_item_in_inventory(state, 'challenge_solved'):
        if not db_is_item_in_inventory(state, 'cursed_magnet'):
            print("A shiny magnet is in a locked glass case. The teacher is watching you.")
        else:
            print("The glass case is empty now. The teacher nods approvingly.")

        if command == "look around":
            look_around(state)
            return True
        elif command == "take magnet" and not db_is_item_in_inventory(state, 'cursed_magnet') and db_is_item_in_inventory(state, 'challenge_solved'):
            take("magnet", state)
            print("You take the Cursed Magnet and are ready to move to another room.")
            return True
    else:
        print(f"you failed the challenge, you can come back later")
        time.sleep(2)
        return "go back"

def look_around(state):
    if not db_is_item_in_inventory(state, 'cursed_magnet'):
        print("The magnet is in a locked glass case. The chalkboard reads: 'Solve the challenge to unlock it.'")
    else:
        print("The classroom is empty except for the usual lab equipment. You are ready to move on.")

def take(item, state):
    if item == "magnet":
        if db_is_item_in_inventory(state, 'challenge_solved'):
            db_add_item_to_inventory(state, 'cursed_magnet')
            db_mark_room_completed(state, "riddle_room")
            print("You take the magnet and add it to your inventory.")
        else:
            print("The magnet is locked. Solve the challenge first.")



def complex_challenge(state):
    if db_is_item_in_inventory(state, 'challenge_solved'):
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

    attempts = 3

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
            print(f"Wrong. Make sure to enter a word or a number as your answer. Attempts left: {attempts}")
    else:
        print("The teacher shakes his head. Come back when you're wiser.")
        return False

    if attempts > 2:
        db_award_achievement(state, 'einstein')

    # --- STEP 2: LOGIC PUZZLE --- #
    print("\n--- Logic Puzzle ---")
    print("Three friends (Alice, Bob, and Carol) are sitting in a row.")
    print("Bob is not at either end. Carol is not next to Alice. Who is sitting in the middle?")
    logic_answer = input("Your answer: ").strip().lower()

    if logic_answer != "bob":
        print("Incorrect. The puzzle resets.")
        return False
    else:
        print("Correct! You're sharp.")

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
        db_add_item_to_inventory(state, "challenge_solved")
        return True
    else:
        print("Incorrect code. The challenge remains unsolved.")
        return False



