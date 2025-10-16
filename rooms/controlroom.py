# -----------------------------------------------------------------------------
# File: rooms/controlroom.py
# Room: Control Room (keycard + cable puzzle)
# -----------------------------------------------------------------------------

def ask_until_correct(question, correct_answer, error_msg="Incorrect, try again."):
    answer = ""
    while answer != correct_answer:
        answer = input(question).strip()
        if answer != correct_answer:
            print(error_msg)
    print("Correct!")
    return answer

def controlroom_enter(state):
    print("You enter the control room.")
    print("You see a keycard on the floor.")
    print("The door you just came through is now closed.\n")
    print("Basic commands: show, look around, continue, go back")
    return True

def controlroom_commands(cmd, state):

    if cmd in ["show", "look around"]:
        print("You see a keycard and a laptop.")
        return True
    elif cmd == "continue":
        print("You move forward to the puzzle.")
        puzzle(state)
        return "go back"

def puzzle(state):
    print("\nSolve these number challenges:")
    ans1 = ask_until_correct("What number comes next in the sequence 3, 6, 12, 24, __? ", "48")
    ans2 = ask_until_correct("Which number doesn't belong: 14, 21, 28, 35, 40? ", "40")
    ans3 = ask_until_correct("How much is the answer to 3 x 5 + 21? ", "36")

    password = ans1 + ans2 + ans3
    print(f"\nThe laptop is password protected. Password = answers combined")

    attempt = ""
    while attempt != password:
        attempt = input("Enter the password to unlock the laptop: ").strip()
        if attempt != password:
            print("Wrong password, try again.")
    print("Laptop unlocked! Final question:")

    ask_until_correct("What is the only even prime number? ", "2")
    print("Correct! You found the keycard to continue.")

    state["has_keycard"] = True
    state["completed"]["controlroom"] = True
    return
