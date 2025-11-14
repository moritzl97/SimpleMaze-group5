# --- Adventure Game: Riddle Room ---
import random
import time
from game.utils import *
from game.db_utils import *

def riddleroom_enter(state):
    if not db_is_item_in_inventory(state, '?_key'):
        print("You try to enter the door to the Riddle Room. However, it is locked with a huge padlock with a peculiarly shaped keyhole that locks like a question mark.")
        return False
    else:
        print("When you enter the room you hear a voice from the loudspeaker:")
        print("Loudspeaker: Welcome to the Room of Riddles!")
        print("You see a slot machine with a single screen and a huge lever.")
        print("In the middle of the room is a pedestal and on it sits a Magnet protected behind a glass dome.")
        return True

def riddleroom_commands(command, state):
    if command in ["pull", "pull lever"]:
        if not db_get_flag(state, "challenge_solved"):
            solved = complex_challenge(state)
            if not solved:
                time.sleep(2)
                return "go back"
        else:
            print("You have already solved the challenge and are ready to move on. However, when you pull the lever the slot machine starts spinning:")
            slot_machine(state)
        return True
    elif command == "look around":
        look_around(state)
        return True
    elif command.startswith("take"):
        take_magnet(state)
        return True
    elif command in ["help", "?"]:
        handle_help(state)
        return True
    return False

def handle_help(state):
    print("\nRiddle Room commands:")
    print("- look around         : Look around in the room")
    print("- pull lever          : Pull the lever of the slot machine")
    print("- take magnet         : Take the magnet")

def look_around(state):
    if not db_is_item_in_inventory(state, 'cursed_magnet'):
        if db_get_flag(state, "challenge_solved"):
            print("The glass case is open and the Magnet ready for the taking.")
        else:
            print("The shiny magnet is in a locked glass case. A big arrow with glowing lights points to the slot machine with a big lever.")
    else:
        print("With the magnet in your pocket you are ready to move on to another room. However, you could also pull the lever of the slot machine once again...")

def take_magnet(state):
    if db_get_flag(state, "challenge_solved"):
        if not db_is_item_in_inventory(state, 'cursed_magnet'):
            db_add_item_to_inventory(state, 'cursed_magnet')
            db_mark_room_completed(state, "riddle_room")
            print("You take the Cursed Magnet and are ready to move to another room.")
        else:
            print("The pedestal is empty.")
    else:
        print("The magnet is locked behind glass. Try to solve the riddle challenge first!")

def slot_machine(state):
    # Emoji symbols for the slot machine reels
    symbols = ['🍒', '🍋', '🍉', '⭐', '🔔', '7️⃣']

    # Spin the slot machine by randomly selecting three symbols
    reel1 = random.choice(symbols)
    reel2 = random.choice(symbols)
    reel3 = random.choice(symbols)

    # Show the result of the spin
    print(f"🎰 {reel1} | {reel2} | {reel3} 🎰")

    # Determine if the player wins
    if reel1 == reel2 == reel3:
        print("Clink, clink, clink!")
        if reel1 == '7️⃣':
            print("🎉SUPER JACKPOT!🎉")
            print("Money is raining from the ceiling. You pick some up, but are not sure on what to use it in this place.")
            db_add_item_to_inventory(state, "money")
        else:
            print("Jackpot! You won! 🎉")
        print("Have you already spend to much time in this room?")
        db_award_achievement(state, "jackpot")
    elif reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
        print("Nice! Two in a row!")
    else:
        print("No win. Try again!")

def complex_challenge(state):
    print("You pull the lever and a happy tune starts to play. The screen turns on and shows:")
    print(f"\n{Color.yellow}### Riddle Challenge ###{Color.end}")

    quizzes = [
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
    logic_puzzles = [
        {
            "question": "Three friends (Alice, Bob, and Carol) are sitting in a row. Bob is not at either end. Carol is not next to Alice. Who is sitting in the middle?",
            "answer": "bob",
        },
        {
            "question": "Three siblings (Jack, Kate, and Liam) are sitting around a circular table. Jack is not next to Liam. Kate is opposite Jack. Who is sitting to the left of Kate?",
            "answer": "liam",
        },
        {
            "question": "Four colleagues (David, Emma, Fiona, and George) are sitting in a row. Emma is not at either end. George is to the immediate right of David. Fiona is not next to George. Who is sitting at the left end?",
            "answer": "fiona",
        }
    ]
    true_or_false = [
        {
            "question": "Statement: 'All dogs are mammals, and some mammals are not dogs.' Question: Is this statement true or false?",
            "answer": "true",
        },
        {
            "question": "Statement: 'If it is raining, then the ground is wet. The ground is wet. Therefore, it is raining.' Question: Is this statement true or false?",
            "answer": "false",
        },
        {
            "question": "Statement: 'The statement 'This statement is false' is true.' Question: Is this statement true or false?",
            "answer": "false",
        }
    ]

    selected_quiz = random.choice(quizzes)
    selected_logic_puzzle = random.choice(logic_puzzles)
    selected_true_or_false = random.choice(true_or_false)

    max_wrong_attempts = 3
    wrong_attempts = 0

    while wrong_attempts < max_wrong_attempts:
        print(f"\n{Color.purple}--- Quiz ---{Color.end}")
        print(f"{selected_quiz['question']}")
        for i, option in enumerate(selected_quiz["options"], start=1):
            print(f" - {option.capitalize()}")
        riddle_answer = input("Your answer (or type 'hint'): ").strip().lower()
        if riddle_answer == "hint":
            print(f"HINT: {selected_quiz['hint']}")
            continue
        if riddle_answer == selected_quiz["answer"]:
            print(f"{Color.green}Correct!{Color.end} Well done.")
            break
        else:
            wrong_attempts += 1
            print(f"{Color.red}Wrong answer.{Color.end} Attempts left: {max_wrong_attempts - wrong_attempts}")

    while wrong_attempts < max_wrong_attempts:
        print(f"\n{Color.purple}--- Logic Puzzle ---{Color.end}")
        print(f"{selected_logic_puzzle['question']}")
        logic_answer = input("Your answer: ").strip().lower()
        if logic_answer == selected_logic_puzzle["answer"]:
            print(f"{Color.green}Correct!{Color.end} You're sharp.")
            break
        else:
            wrong_attempts += 1
            print(f"{Color.red}Wrong answer.{Color.end} Attempts left: {max_wrong_attempts - wrong_attempts}")

    while wrong_attempts < max_wrong_attempts:
        print(f"\n{Color.purple}--- True or False Riddle---{Color.end}")
        print(f"{selected_true_or_false['question']}")
        true_or_false_answer = input("Your answer: ").strip().lower()
        if true_or_false_answer == selected_true_or_false["answer"]:
            print(f"{Color.green}Correct!{Color.end} True or False solved!")
            break
        else:
            wrong_attempts += 1
            print(f"{Color.red}Wrong answer.{Color.end} Attempts left: {max_wrong_attempts - wrong_attempts}")

    while wrong_attempts < max_wrong_attempts:
        print(f"\n{Color.purple}--- Final Code ---{Color.end}")
        print("Combine: first letter of quiz answer + number of letters in the logic puzzle answer. Reverse the order if the True or False Riddle was False.")
        if selected_logic_puzzle["answer"]:
            expected_code = (str(len(selected_logic_puzzle["answer"]))+ selected_quiz["answer"][0])
        else:
            expected_code = (selected_quiz["answer"][0] + str(len(selected_logic_puzzle["answer"])))


        final_input = input("Enter the code: ").strip().lower()
        if final_input == expected_code:
            print(f"🔓 {Color.green}Password correct!{Color.end} The glass case clicks open. You can now take the magnet!")
            db_set_flag(state, "challenge_solved", True)
            break
        else:
            wrong_attempts += 1
            print(f"{Color.red}Wrong answer.{Color.end} Attempts left: {max_wrong_attempts - wrong_attempts}")

    if wrong_attempts >= max_wrong_attempts:
        print("You ran out of attempts and failed the challenge.")
        print("The slot machine begins to smoke. Best to leave and come back again later.")
        return False
    else:
        if wrong_attempts == 0:
            db_award_achievement(state, 'einstein')
        return True




