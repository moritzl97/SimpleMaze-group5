# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================


import random
import time
from game.db_utils import *
from game.db import *
from game.utils import *
from rooms.computer_lab_db_utils import *


intercultural_questions = [
    ("When working with a team from different cultures, what is the best approach? (A) respect the differences and communicate openly, (B) assume everyone communicates the same way, (C) avoid discussing anything", ["a", "respect the differences and communicate openly"]),
    ("You notice a team member is uncomfortable sharing their opinion due to cultural differences. What should you do? (A) ignore it to avoid awkwardness, (B) encourage them, (C) let others dominate the discussion", ["b", "encourage them"]),
    ("What is key to successful intercultural collaboration? (A) speaking louder for clarity, (B) assuming others will adapt to your style, (C) empathy and understanding", ["c", "empathy and understanding"]),
    ("How can you handle misunderstandings that arise due to cultural differences? (A) stop collaborating with them, (B) clarify politely and listen actively, (C) blame the other person for miscommunication", ["b", "clarify politely and listen actively"]),
    ("How can leaders support intercultural collaboration? (A) discourage cultural discussions to stay neutral, (B) enforce one cultural standard for everyone, (C) promote inclusivity and model open communication", ["c", "promote inclusivity and model open communication"]),
    ("What is the main benefit of intercultural collaboration? (A) it leads to innovation through diverse perspectives, (B) it increases misunderstandings and delays, (C) it makes decision-making slower and harder", ["a", "it leads to innovation through diverse perspectives"])
]

python_questions = [
    ("What is the output of print(3 + 4 * 2)?", ["11"]),
    ("Which of these is a valid Python variable name? (A) 2fast (B) fast_2 (C) fast-2", ["b", "fast_2"]),
    ("What does len('Python') return?", ["6"]),
    ("Which keyword is used to define a function in Python? (A) function, (B) def, (C) func", ["b", "def"]),
    ("How do you start a comment in Python? (A) /*, (B) //, (C) #", ["c", "#"]),
    ("Which of the following creates a dictionary? (A) {1: 'a', 2: 'b'}, (B) (1: 'a', 2: 'b'), (C) [1: 'a', 2: 'b']", ["a", "{1: 'a', 2: 'b'}"])
]

database_questions = [
    ("Which SQL command retrieves data from a table? (A) SELECT, (B) DELETE, (C) INSERT", ["a", "select"]),
    ("Which SQL clause is used to filter rows? (A) WHERE, (B) FROM, (C) GROUP BY", ["a", "where"]),
    ("A table has columns: ID, Name, Age. Which is a primary key?", ["id"]),
    ("What does the INSERT command do in SQL? (A) deletes rows from a table, (B) adds new rows to a table, (C) retrieves data from a table", ["b", "adds new rows to a tabl"]),
    ("What keyword combines rows from two or more tables based on a related column? (A) MERGE, (B) LINK, (C) JOIN", ["c", "join"]),
    ("Which SQL command is used to change a table’s structure? (A) UPDATE TABLE, (B) ALTER TABLE, (C) CHANGE TABLE", ["b", "alter table"])
]

professional_questions = [
    ("Best way to handle conflict with a colleague? (A) avoid them until the issue goes away, (B) communicate directly and discuss the issue calmly, (C) complain to everyone else about the problem", ["b", "communicate directly and discuss the issue calmly"]),
    ("How can you improve your communication skills at work? (A) practice active listening and clear expression, (B) talk more loudly to be notice, (C) avoid giving feedback to others", ["a", "practice active listening and clear expression"]),
    ("Receiving feedback: which is the best approach? (A) defend yourself immediately, (B) ignore it if it feels uncomfortable, (C) listen openly and reflect before responding", ["c", "listen openly and reflect before responding"]),
    ("If you make a mistake at work, what should you do? (A) deny responsibility, (B) admit it, apologize, and correct it, (C) blame someone else", ["b", "admit it apologize and correct it"]),
    ("If someone upsets you, what should you do first? (A) take a moment before responding calmly, (B) reply immediately with your emotions, (C) forward it to everyone in frustration", ["a", "take a moment before responding calmly"]),
    ("What’s the best way to handle a missed deadline? (A) say nothing and hope they don’t notice, (B) blame technical issues, (C) inform your supervisor early and provide a plan to catch up", ["c", "inform your supervisor early and provide a plan to catch up"])
]


def computer_lab_enter(state):
    cl_get_state(state)
    print("\n💻 You step into the computer lab.")
    if db_mark_room_completed(state, "computer_lab"):
        print(f"\n{Color.bold}You've already finished this room!{Color.end}")
        return False
    print("The room is dead silent. There's only one person working on their computer.")
    print("The said person looks up to look at you, but immediately turns their gaze towards the computer again.")

    return True

def handle_look():
    print("\n👀 You take a look around.")
    print("Rows of desks stretch out before you.")
    print("\nOn every desk sits a dark monitor, a small keyboard, a mouse, and computers. None of them are powered on — the room feels strangely asleep.")
    print("Colorful posters cover the remaining walls, each one shouting about programming languages, networking, and other IT mysteries.")
    print("On the right, you see a projector that is connected to a small device, a laptop. The screen glows brightly, there's something written on it.")
    print("On the left, a large whiteboard is plastered with sticky notes. Many are half-peeled or scattered across the floor, as if they’ve given up holding on.")
    print("Maybe you should talk to the student about the laptop?")
    print("Before you could decide, a small silhouette runs past you and sits in the corner of the room.")


def handle_talk(target, state):
    if target == "silhouette":
        print("\nYou walk towards the silhouette that's sitting in the corner of the room.")
        print("Upon further inspection you see it's a... gnome?")
        print(f"{Color.red}⣿⣿⣿⣿⣿⠟⠉⠁⠄⠄⠄⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⠏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠸⢿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣏⠄⡠⡤⡤⡤⡤⡤⡤⡠⡤⡤⣸⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣗⢝⢮⢯⡺⣕⢡⡑⡕⡍⣘⢮⢿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⡧⣝⢮⡪⡪⡪⡎⡎⡮⡲⣱⣻⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⠟⠁⢸⡳⡽⣝⢝⢌⢣⢃⡯⣗⢿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⠟⠁⠄⠄⠄⠹⡽⣺⢽⢽⢵⣻⢮⢯⠟⠿⠿⢿⣿⣿⣿⣿⣿")
        print("⡟⢀⠄⠄⠄⠄⠄⠙⠽⠽⡽⣽⣺⢽⠝⠄⠄⢰⢸⢝⠽⣙⢝⢿")
        print("⡄⢸⢹⢸⢱⢘⠄⠄⠄⠄⠄⠈⠄⠄⠄⣀⠄⠄⣵⣧⣫⣶⣜⣾")
        print("⣧⣬⣺⠸⡒⠬⡨⠄⠄⠄⠄⠄⠄⠄⣰⣿⣿⣿⣿⣿⣷⣽⣿⣿")
        print("⣿⣿⣿⣷⠡⠑⠂⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⣄⠠⢀⢀⢀⡀⡀⠠⢀⢲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⣿⢐⢀⠂⢄⠇⠠⠈⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⣧⠄⠠⠈⢈⡄⠄⢁⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⣿⡀⠠⠐⣼⠇⠄⡀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print("⣿⣿⣿⣿⣯⠄⠄⡀⠈⠂⣀⠄⢀⠄⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print(f"⣿⣿⣿⣿⣿⣶⣄⣀⠐⢀⣸⣷⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿{Color.end}")
        print("\n\n... What the hell?")
        db_award_achievement(state, 'gnomed')
        return None

    if target == "student":
        if cl_check_riddle_answer(state):
            print(f"\n👩 {Color.bold}{Color.orange}It's you again, didn't I help you already? {Color.end}")
        else:
            print("\nThe student turns around to face you. Confusion plastered on their face.")
            print(f"\n👩 {Color.bold}{Color.orange}Um, is there anything I can help you with? {Color.end}")
    else:
        print(f"❌ There is no {target} here to talk to.")


def handle_ask(target, state):
    if target == "student":
        if cl_check_riddle_answer(state):
            print("\n\tThe student looks annoyed at you.")
            print(f"{Color.orange}{Color.bold}👩 Did you forget the password? It's crypt0. {Color.end}")
            return None
        else:
            print(f"\n{Color.orange}{Color.bold}👩 Oh, the laptop? Yeah, I know the password, but I need you to solve my riddle first! {Color.end}")
            print(f"\n\n{Color.underline}I'm made of only ones and zeros,")
            print("yet I can store music, pictures and prose.")
            print(f"What am I?{Color.end}")

            response = input("\nYour answer: ").strip().lower()
            normalized = response
            if normalized in ["binary", "binary code", "bits"]:
                print("\nThe student smiles.")
                print(f"\n👩 {Color.orange}{Color.bold}Yeah, that's right! I was curious if you knew ")
                print("👩 Anyway, the password to the laptop is: crypt0 ")
                print(f"👩 Don't forget it! {Color.end}")
                cl_set_riddle_answer(state, True)
                print("\nYou managed to successfully obtain the password.")
                print("It's worth to check out that laptop out.")
            else:
                print("\n\tThe student looks amused.")
                print(f"\n👩 {Color.orange}{Color.bold}Yeah, I think you need to think it over {Color.end}")
                print("You return to the corridor in shame")
                return None
    else:
        print(f"❌ There is no {target} here to ask")

def play_two_random_questions(seminar_name, questions_list):
    # asks 4 questions when you open one of the folders
    selected_questions = random.sample(questions_list, 4)
    for idx, (question, answers) in enumerate(selected_questions, 1):
        while True:
            answer = input(f"\n{seminar_name} Question {idx}:\n{question}\nYour answer: ").strip().lower()
            if any(ans in answer for ans in answers):
                print(f"✅ {Color.green}Correct!{Color.end}\n")
                break
            else:
                print(f"❌ {Color.red}Incorrect! Try again.{Color.end}\n")

def handle_interact(state):
    # checks if the laptop is still locked
    current_time = time.time()
    lock_time = cl_check_softlock_value(state)
    if lock_time is not None and current_time < lock_time:
        remaining = lock_time - current_time
        print(f"{Color.red}----------------------------------------------------------------")
        print(f"🚫 The laptop is still locked! Try again in {remaining} seconds.")
        print(f"----------------------------------------------------------------{Color.end}")
        return None

    if cl_is_laptop_unlocked(state):
        print("\nYou open the laptop again.")
        laptop_screen(state)
        return None
    else:
        print("\n💻You inspect the laptop.")
        print("There's nothing specific about it")
        print("The background appears to be a small, black cat looking up at whoever took the picture.")
        print("In the centre of the screen you see a notification")
        print(f"\n{Color.blue}             Enter the password{Color.end}")
        print("You think to yourself for a moment... What's the password?")

    attempts = 3
    while attempts > 0:
        password_input = input("\nEnter the password: ").strip()
        password = "crypt0"
        if password_input == password:
            print(f"\n✅ {Color.green}Correct! You've gained access to the laptop.{Color.end}")
            cl_set_laptop_unlocked(state, True)
            laptop_screen(state)
            break
        else:
            attempts -= 1
            if attempts > 0:
                print(f"❌ {Color.red}Incorrect password! Attempts left: {attempts}{Color.end}")
            else:
                cl_set_softlock_value(state, 30)
                lock_time = cl_check_softlock_value(state) # the laptop gets locked after getting the password wrong 3 times
                print("\n🚫 The laptop has been locked for 30 seconds after too many failed attempts.")
                remaining = lock_time - time.time()
                print(f"{Color.red}--------------------------------------------")
                print(f"⏳ {remaining} seconds remaining.")
                print(f"--------------------------------------------{Color.end}")
                return None

def laptop_screen(state):
    print(f"\nOn the screen, you see folders labelled {Color.bold}'Intercultural Collaboration', 'Database & Data Structures', 'Professional Skills', 'Python Programming'{Color.end}")
    print("There also appears to be a fifth folder, which is locked behind a password.")
    print("Below the folders you see txt labelled 'README'")
    while True:
        player_choice = input(f"\nWhat do you want to open first? {Color.bold}(Intercultural Collaboration / Database & Data Structures / Professional Skills / Python Programming / README / Secret Folder / Exit){Color.end}: ").strip().lower()

        if player_choice in ["intercultural collaboration", "1"]:
            if not cl_is_seminar_completed(state, 'intercultural collaboration'):
                print("\n📂 You've opened the folder called Intercultural Collaboration.")
                print("\nImmediately after opening the folder u get a pop up window.\n")
                print(f"{Color.framed} ")
                print("In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions.")
                print(f" {Color.end} ")
                play_two_random_questions("Intercultural Collaboration", intercultural_questions) # plays 4 randomized questions
                cl_mark_seminar_completed(state, 'intercultural collaboration')
                print(f"✅ {Color.green}You obtained the key fragment from this folder!{Color.end}\n")
                print(f"{Color.blue}ac__ ___ h___{Color.end}")
            else:
                print("\n📂 You've already completed this folder and collected the key fragment.")

        elif player_choice in ["database & data structures", "2"]:
            if not cl_is_seminar_completed(state, 'database & data structures'):
                print("\n📂 You've opened the folder called Database & Data Structures.")
                print("\nImmediately after opening the folder u get a pop up window.\n")
                print(f"{Color.framed} ")
                print("In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions.")
                print(f" {Color.end} ")
                play_two_random_questions("Database & Data Structures", database_questions) # plays 4 randomized questions
                cl_mark_seminar_completed(state, 'database & data structures')
                print(f"✅ {Color.green}You obtained the key fragment from this folder!{Color.end}\n")
                print(f"{Color.blue}__es f__ ____{Color.end}")
            else:
                print("\n📂 You've already completed this folder and collected the key fragment.")


        elif player_choice in ["professional skills", "3"]:
            if not cl_is_seminar_completed(state, 'professional skills'):
                print("\n📂 You've opened the folder called Professional Skills.")
                print("\nImmediately after opening the folder u get a pop up window.\n")
                print(f"{Color.framed} ")
                print("In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions.")
                print(f" {Color.end} ")
                play_two_random_questions("Professional Skills", professional_questions) # plays 4 randomized questions
                cl_mark_seminar_completed(state, 'professional skills')
                print(f"✅ {Color.green}You obtained the key fragment from this folder!{Color.end}\n")
                print(f"{Color.blue}____ _ly ___h{Color.end}")
            else:
                print("\n📂 You've already completed this folder and collected the key fragment.")


        elif player_choice in ["python programming", "4"]:
            if not cl_is_seminar_completed(state, 'python programming'):
                print("\n📂 You've opened the folder called Python Programming.")
                print("\nImmediately after opening the folder u get a pop up window.\n")
                print(f"{Color.framed} ")
                print("In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions.")
                print(f" {Color.end} ")
                play_two_random_questions("Python Programming", python_questions) # plays 4 randomized questions
                cl_mark_seminar_completed(state, 'python programming')
                print(f"✅ {Color.green}You obtained the key fragment from this folder!{Color.end}\n")
                print(f"{Color.blue}____ ___ _ig_{Color.end}")
            else:
                print("\n📂 You've already completed this folder and collected the key fragment.")


        elif player_choice in ["readme", "5"]:
            print("\n📂 You've opened the file README.")
            print(f"\n\t{Color.framed}{Color.bold}--------------- INSTRUCTION ---------------")
            print(f"Congratulations on unlocking the laptop!")
            print("You're halfway there :^)")
            print("In order to progress further you have to finish the previous 4 folders.")
            print("Each folder contains questions that you have to solve.")
            print("If you answer correctly you'll get a key fragment that is needed to unlock the secret folder.")
            print("Please make sure to write everything on your paper!!")
            print(f"\t                Good luck!                                                            {Color.end}")


        elif player_choice in ["secret folder", "6"]:
            if not cl_are_all_seminars_completed(state): # checks if the player finished the folders first
                print("\n🔒 You need to finish all the folders first before attempting to unlock the folder!")
            else:
                print("\n📂 You've opened the folder called Secret Folder.")
                password = input("Please enter the password: ").strip().lower().replace(" ", "")
                if password == "acesflyhigh":
                    print(f"\n✅ {Color.green}Correct Password!{Color.end}")
                    print(f"\n\n\n\n\n{Color.bold}{Color.underline}CONGRATULATIONS! You've managed to finish all the puzzles in the Computer Lab!!{Color.end}")
                    print(f"\n\n{Color.bold}WHISTLE{Color.end}")
                    print("You look to your left to see the student standing right next to you.")
                    print(f"\n👩 {Color.orange}{Color.bold}Nice work! Didn't think you had it in you ")
                    print(f"👩 Here, take this! {Color.end}")
                    print("\nThe student hands you a light object.")
                    print("It appears to be a key of some sorts. Maybe you'll be able to use it in the future?")
                    print("Without asking further questions, you take the key and nod towards the student.")
                    print(f"\n👩 {Color.orange}{Color.bold}Good luck on the rest of your adventure! {Color.end}")
                    print(f"\n\n\n\n\n {Color.bold}An item called cloud_key has been added to your inventory.")
                    print("You can check it out by typing inventory in the console.")
                    print("You may now finish the cloud room by going back to the lab corridor.")
                    db_add_item_to_inventory(state, "lab_key")
                    db_mark_room_completed(state, "computer_lab")
                    break
                else:
                    print(f"❌ {Color.red}Incorrect Password! Try again.{Color.end}")


        elif player_choice in ["exit", "leave", "quit"]:
            print("\nYou close the laptop and take a step back.")
            print("You can return to the laptop anytime you want.")
            break
        else:
            print(f"\n❌ {Color.red}That folder doesn't exist. Please try again.{Color.end}")


def handle_help():
        # shows available commands in the room
        print("\nComputer Lab commands:")
        print("- look around         : Examine the room and its contents.")
        print("- talk student        : Talk to the student.")
        print("- ask student         : Ask a student a question.")
        print("- interact laptop     : Interact with the laptop.")

def computer_lab_commands(command, state):

        if command == "look around":
            handle_look()
            return True

        elif command == "?" or command == "help":
            handle_help()
            return True

        elif command.startswith("talk "):
            target = command[5:].strip()
            handle_talk(target, state)
            return True

        elif command.startswith("ask "):
            target = command[4:].strip()
            handle_ask(target, state)
            return True

        elif command.startswith("interact "):
            target = command[9:].strip()
            if target == "laptop":
                handle_interact(state)
                return True
            else:
                print(f"❌ You can't interact with {target}.")
                return True