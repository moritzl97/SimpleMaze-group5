import time
from game.db_utils import db_add_item_to_inventory, db_award_achievement, db_mark_room_completed

EMOJI_QUESTION = "\u2753"  # ❓
EMOJI_WRONG = "\u274C"     # ❌
EMOJI_CORRECT = "\u2705"   # ✅
EMOJI_ROBOT = "\U0001F916" # 🤖
EMOJI_FREEZE = "\u2744"    # ❄️

def ask_until_correct(question, correct_answer, error_msg="Incorrect, try again."):
    attempts = 0
    answer = ""
    while answer != correct_answer:
        answer = input(f"{EMOJI_QUESTION} {question}").strip()
        if answer.lower() == "skip":
            print("Puzzle skipped.")
            return None, False
        if answer != correct_answer:
            attempts += 1
            print(f"{EMOJI_WRONG} {error_msg}")
            if attempts > 1:  # Congela tras más de un fallo
                print(f"{EMOJI_FREEZE} Too many failed attempts! You are blocked for 15 seconds.")
                time.sleep(15)
                print("You can try again.")
    print(f"{EMOJI_CORRECT} Correct!")
    return answer, False

def controlroom_enter(state):
    print("You enter the control room.")
    print("You see a laptop on a desk buzzing softly with light.")
    print("The door you came through is now locked behind you.\n")
    print("Basic commands: show, look around, side quest, continue, go back")
    print("Solve the puzzles to find something useful for your escape...")
    return True

def controlroom_commands(cmd, state):
    if cmd in ["show", "look around"]:
        print("You see a laptop on the desk and some scattered papers.")
        return True
    elif cmd == "side quest":
        side_quest(state)
        return True
    elif cmd == "continue":
        print("You approach the laptop to start the puzzle.")
        puzzle(state)
        return "go back"
    else:
        print("Invalid command. Try: show, look around, side quest, continue, go back.")
        return False

def side_quest(state):
    print(f"{EMOJI_ROBOT} A friendly robot approaches you and says:")
    print('"I can help with your puzzle if you answer this easy question."')
    question = "I grow by adding the same number each time. If you start with 3 and add 3 repeatedly, what is the fourth number? "
    correct_answer = "12"
    while True:
        answer = input(f"{EMOJI_ROBOT} {question}").strip()
        if answer.lower() == "skip":
            print(f"{EMOJI_ROBOT} Robot: Maybe next time!")
            return
        if answer == correct_answer:
            print(f"{EMOJI_CORRECT} Robot: Great job! You have unlocked the 'Robot Master' achievement.")
            db_award_achievement(state, "robot_master")
            print("Hint: Understanding sequences will help solve the laptop puzzle ahead.")
            break
        else:
            print(f"{EMOJI_WRONG} That's not it, try again or type 'skip' to leave the robot.")

def puzzle(state):
    print("\nSolve these number challenges to proceed:")
    ans1, _ = ask_until_correct("What number comes next in the sequence 3, 6, 12, 24, __? ", "48")
    if ans1 is None:
        print("Puzzle exited.")
        return
    ans2, _ = ask_until_correct("Which number doesn't belong: 14, 21, 28, 35, 40? ", "40")
    if ans2 is None:
        print("Puzzle exited.")
        return
    ans3, _ = ask_until_correct("How much is the answer to 3 x 5 + 21? ", "36")
    if ans3 is None:
        print("Puzzle exited.")
        return

    password = ans1 + ans2 + ans3
    print(f"\nThe laptop is password protected. Password = answers combined")

    attempts = 0
    frozen = False
    attempt = ""
    while attempt != password:
        attempt = input("Enter the password to unlock the laptop: ").strip()
        if attempt != password:
            attempts += 1
            print(f"{EMOJI_WRONG} Wrong password, try again.")
            if attempts > 1:
                print(f"{EMOJI_FREEZE} Too many failed attempts! You are blocked for 15 seconds.")
                time.sleep(15)
                print("You can try again.")

    print("Laptop unlocked! Final question:")
    finale, _ = ask_until_correct("What is the only even prime number? ", "2")
    if finale is None:
        print("Puzzle exited.")
        return

    print("Correct! You found a bottle opener that might be useful ahead.")
    db_add_item_to_inventory(state, "bottle_opener")
    db_mark_room_completed(state, "control_room")
    print("\nWith the bottle opener in hand, you feel one step closer to escaping this nightmare.\n")
    print("Now, head back and explore what lies beyond the control room door.")
    time.sleep(3)
    return
