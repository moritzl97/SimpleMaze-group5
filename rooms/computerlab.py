import random


intercultural_questions = [
    ("When working with a team from different cultures, what is the best approach?", ["respect", "communicate", "active listening"]),
    ("You notice a team member is uncomfortable sharing their opinion due to cultural differences. What should you do?", ["encourage", "invite participation"]),
    ("What is key to successful intercultural collaboration?", ["understanding", "empathy"])
]

python_questions = [
    ("What is the output of print(3 + 4 * 2)?", ["11"]),
    ("Which of these is a valid Python variable name? A) 2fast B) fast_2 C) fast-2", ["b", "fast_2"]),
    ("What does len('Python') return?", ["6"])
]

database_questions = [
    ("Which SQL command retrieves data from a table? (A) SELECT, (B) DELETE, (C) INSERT", ["a", "select"]),
    ("Which SQL clause is used to filter rows? (A) WHERE, (B) FROM, (C) GROUP BY", ["a", "where"]),
    ("A table has columns: ID, Name, Age. Which is a primary key?", ["id"])
]

professional_questions = [
    ("Best way to handle conflict with a colleague?", ["communicate", "discussion"]),
    ("You are asked to present a report to your team. What is the first thing you should do?", ["prepare", "plan"]),
    ("Receiving feedback: which is the best approach?", ["listen", "open"])
]

password = "crypt0"
laptop_unlocked = False


def computerlab_enter(state):
    print("\n💻 You step into the computer lab.")
    print("The room is dead silent. There's only one person working on their computer.")
    print("The said person looks up to look at you, but immediately turns their gaze towards the computer again.")
    if state ["completed"]["computerlab"]:
        print("You've already finished this room.")
    return True

def handle_look():
    print("\n\t👀 You take a look around.")
    print("\nRows of desks stretch out before you.")
    print("\nOn every desk sits a dark monitor, a small keyboard, a mouse, and computers. None of them are powered on — the room feels strangely asleep.")
    print("Colorful posters cover the remaining walls, each one shouting about programming languages, networking, and other IT mysteries.")
    print("On the right, you see a projector that is connected to a small device, a laptop. The screen glows brightly, there's something written on it.")
    print("On the left, a large whiteboard is plastered with sticky notes. Many are half-peeled or scattered across the floor, as if they’ve given up holding on.")
    print("Maybe you should talk to the student about the laptop?")

def handle_talk(target, state):
    if target == "student":
        print("\n\t The student turns around to face you. Confusion plastered on their face.")
    else:
        print(f"❌There is no {target} here to talk to.")
    if not state["completed"]["computerlab"]:
        print("\n👩'Um, is there anything I can help you with?'")
    else:
        print("\n👩'It's you again, didn't I help you already?")

def handle_ask(target, state):
    if state["completed"]["computerlab"]:
        print("\n\tThe student looks annoyed at you.")
        print("👩'Did you forget the password? It's crypt0.'")
        return None
    if target == "student":
        print("\n\t👩'Oh, the laptop? Yeah, I know the password, but I need you to solve my riddle first.'")
        print("\nI'm made of only ones and zeros,")
        print("yet I can store music, pictures and prose.")
        print("What am I?")
    else:
        print(f"❌There is no {target} here to ask")

def handle_answer(response, state):
    if state["completed"]["computerlab"]:
        print(f"The student looks annoyed and decides to ignore you.")
        return None
    normalized = response.lower().strip()
    if normalized in ["binary", "binary code", "bits"]:
        print("\n\tThe student smiles.")
        print("\n👩'Yeah, that's right! I was curious if you knew.'")
        print("👩'Anyway, the password to the laptop is: crypt0'")
        print("👩'Don't forget it!'")
        print("\n\tYou managed to successfully obtain the password.")
        print("\tIt's worth to check out that laptop out.")
        state["completed"]["computerlab"] = True
    else:
        print("\n\tThe student looks amused.")
        print("\n👩'Yeah, I think you need to think it over.'")
        print("You return to the corridor in shame.")
        return "go back"

def play_two_random_questions(seminar_name, questions_list):
    selected_questions = random.sample(questions_list, 2)  # pick 2 random tuples
    for idx, (question, answers) in enumerate(selected_questions, 1):
        while True:
            answer = input(f"\n{seminar_name} Question {idx}:\n{question}\nYour answer: ").strip().lower()
            if any(ans in answer for ans in answers):
                print("✅ Correct!\n")
                break
            else:
                print("❌ Incorrect! Try again.\n")

def handle_interact(state):
    global laptop_unlocked
    if state["completed"]["computerlab"]:
        print("You're already finished with the puzzle.")
        return None
    else:
        print("\nYou inspect the laptop.")
        print("There's nothing specific about it")
        print("The background appears to be a small, black cat looking up at whoever took the picture.")
        print("In the centre of the screen you see a notification")
        print("\n Enter the password")
        print("You think to yourself for a moment... What's the password?")
        attempts = 3

    while attempts > 0:
        password_input = input("\nEnter the password: ").strip()
        if password_input == password:
            print("\n✅ Correct! You've gained access to the laptop.")
            laptop_unlocked = True
            break
        else:
            attempts -= 1
            if attempts > 0:
                print(f"❌ Incorrect password! Attempts left: {attempts}")

    if not laptop_unlocked:
        print("\n🚫 The laptop locks you out after too many failed attempts.")
        return None

    completed_seminars = {
        "intercultural collaboration": False,
        "python programming": False,
        "database & data structures": False,
        "professional skills": False
    }

    print("\nOn the screen, you see folders labelled 'Intercultural Collaboration', 'Database & Data Structures', 'Professional Skills', 'Python Programming'")
    print("There also appears to be a fifth folder, which is locked behind a password.")
    print("Below the folders you see txt labelled 'README'")
    while True:
        player_choice = input("\nWhat do you want to open first? (Intercultural Collaboration / Database & Data Structures / Professional Skills / Python Programming / README): ").strip().lower()

        if player_choice in ["Intercultural Collaboration", "1"]:
            if not completed_seminars["intercultural collaboration"]:
                print("\n📂 You've opened the folder called Intercultural Collaboration.")
                print("Immediately after opening the folder u get a pop up window.")
                print("'In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions'.")
                play_two_random_questions("Intercultural Collaboration", intercultural_questions)
                completed_seminars["intercultural collaboration"] = True
                print("✅ You obtained the key fragment from this folder!\n")
                print(".")
            else:
                print("\n📂 You've already completed this folder and collected the key fragment.")

        elif player_choice in ["Database & Data Structures", "2"]:
            if not completed_seminars["database & data structures"]:
                print("\n📓 You've opened the folder called Database & Data Structures.")
                print("Immediately after opening the folder u get a pop up window.")
                print("'In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions'.")

        elif player_choice in ["Professional Skills", "3"]:
            if not completed_seminars["professional skills"]:
                print("\n🔒 You've opened the folder called Professional Skills.")
                print("Immediately after opening the folder u get a pop up window.")
                print("'In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions'.")

        elif player_choice in ["Python Programming", "4"]:
            if not completed_seminars["python programming"]:
                print("\n🔒 You've opened the folder called Python Programming.")
                print("Immediately after opening the folder u get a pop up window.")
                print("'In order to obtain a fragment of the hidden key to the locked folder you have to finish 2 questions'.")

        elif player_choice in ["README", "readme", "5"]:
            print("\n🔒 You've opened the file README.")
            print(".")

        elif player_choice in ["exit", "leave", "6"]:
            print("\nYou close the laptop and take a step back.")
            break
        else:
            print("\n❌ That folder doesn't exist. Please try again.")



def handle_help():
    print("- look around         : Examine the room and its contents.")
    print("- talk student        : Talk to the student.")
    print("- ask student         : Ask a student a question.")
    print("- answer              : Answer the question.")
    print("- interact laptop     : Interact with the laptop.")

def computerlab_commands(command, state):

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

    elif command.startswith("answer "):
        response = command[7:].strip()
        result = handle_answer(response, state)
        if result:
            return result
        else:
            return True

    elif command.startswith("interact "):
        target = command[9:].strip()
        if target == "laptop":
            handle_interact(state)
            return True
        else:
            print(f"❌ You can't interact with {target}.")
            return True
