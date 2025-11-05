import time
from game.db_utils import *

EMOJI_QUESTION = "\u2753"  # ❓
EMOJI_WRONG = "\u274C"     # ❌
EMOJI_CORRECT = "\u2705"   # ✅
EMOJI_ROBOT = "\U0001F916" # 🤖
EMOJI_FREEZE = "\u2744"    # ❄️

def controlroom_enter(state):
    print("You enter the control room.")
    print("All walls are covered in screens. You see buttons and levers controlling all sorts of systems in the school.")
    print("A big machine stands in the middle of the room. Gears are turning and the machine is clicking.")
    print("However, something seams not quite to work correctly.")
    return True

def controlroom_commands(cmd, state):
    if cmd == "look around":
        if not db_get_room_completed(state, "control_room"):
            print("The machine in the middle of the room needs repairs.")
        print("One screen on the wall is pitch black. Behind it you see a robot with a soldering device fixing some electronics.")
        return True
    elif cmd in ["?", "help"]:
        handle_help(state)
        return True
    elif cmd in ["talk robot", "look robot", "robot"]:
        side_quest(state)
        return True
    elif cmd in ["repair", "repair machine"]:
        puzzle(state)
        return True
    return False

def handle_help(state):
    print("\nControl Room commands:")
    print("- look around         : Looks around in the North South corridor")
    print("- talk robot          : Speak with the robot")
    print("- repair machine      : Repair the big machine")

def wait(seconds):
    # Wait for input seconds
    for i in range(seconds, 0, -1):
        # print the whole line each time, start with \r to return to line start
        print(f"\r{EMOJI_FREEZE} You are stunned for {i} seconds.  ", end='', flush=True)
        time.sleep(1)
    print("\nYou shake it off and can act again.")

def ask_until_correct(question, correct_answer):
    attempts = 0
    answer = ""
    while answer != correct_answer:
        answer = input(f"{EMOJI_QUESTION} {question} ").strip()
        if answer.lower() == "skip":
            print("Puzzle skipped.")
            return None
        if answer != correct_answer:
            attempts += 1
            print(f"{EMOJI_WRONG} Incorrect, try again.")
            if attempts > 1:
                print("Too many failed attempts!")
                wait(5)
                print("You can try again.")
    print(f"{EMOJI_CORRECT} Correct!")
    return answer

def side_quest(state):
    if db_get_flag(state, "side_quest_completed"):
        print("The robot doesn't respond anymore.")
        return
    print("Behind a damaged screen stands a robot. The robot stares on a small screen with a loading bar stuck at 99%.")
    print("As you approach it looks up to you.")
    print(f'{EMOJI_ROBOT}: My calculation chip got damaged. Can you help me out with the final problem?')
    correct_answer = "12"
    answer = input(f"{EMOJI_ROBOT}: The number I am looking for grows by adding the same number each time. If you start with 3 and add 3 repeatedly, what is the fourth number? ").strip().lower()
    print(f"The robot types in the answer {answer} into his terminal.")
    if answer == correct_answer:
        print("It displays 100%")
        print(f"{EMOJI_ROBOT}: {EMOJI_CORRECT} Great job! Thank you for helping me!")
        db_award_achievement(state, "robot_master")
    else:
        print(f"{EMOJI_WRONG} The progress bar stays stuck 99%. The robots eyes are fixed on the progress bar and it doesn't answer anymore.")
    db_set_flag(state, "side_quest_completed", True)

def puzzle(state):
    if db_get_room_completed(state, "control_room"):
        print("You already fixed the machine and are ready to move on to another room.")
        return

    print("You see different gears with numbers on them locked together. However, the last one is missing.")
    ans1 = ask_until_correct("The numbers on the gears are 3, 6, 12 and 24. Which number should the last gear show?", "48")
    if ans1 is None:
        print("Puzzle exited.")
        return
    print("Five levers that direct electricity are turned on.")
    ans2 = ask_until_correct("The levers are labeled with numbers 14, 21, 28, 35 and 40. Which lever doesn't belong and should be turned of? ", "40")
    if ans2 is None:
        print("Puzzle exited.")
        return
    print("A screen and a keyboard folds out from the inside the machine.")
    ans3 = ask_until_correct("The screen shows the math equation 3 x 5 + 21. What number should you enter? ", "36")
    if ans3 is None:
        print("Puzzle exited.")
        return

    password = ans1 + ans2 + ans3
    print("The last thing to do to repair the machine is to enter the final password.")

    ask_until_correct("Combine all three answers from before to a 6 digit code.", password)

    print("The machine starts to hum melodically. In the machine you find the cause of the malfunction. A bottle opener was jammed in between two gears.")
    print("You are not sure how it will help you in the future, but you add it to your inventory. Now it is time to head back and explore what lies beyond the control room.")
    db_add_item_to_inventory(state, "bottle_opener")
    db_mark_room_completed(state, "control_room")
    return
