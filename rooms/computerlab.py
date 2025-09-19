import sys


def enterComputerlab(state):
    print("\n💻 You step into the computer lab.")
    print("The room is dead silent. There's only one person working on their computer.")
    print("The said person looks up to look at you, but immediately turns their gaze towards the computer again.")

    def handle_look():
        print("\n👀 You take a look around.")
        print("Rows of desks stretch out before you. On every desk sits a dark monitor, a small keyboard, a mouse, and computers. None of them are powered on — the room feels strangely asleep.")
        print("Colorful posters cover the remaining walls, each one shouting about programming languages, networking, and other IT mysteries.")
        print("On the right, you see a projector that is connected to a small device, a laptop. The screen glows brightly, there's something written on it.")
        print("On the left, a large whiteboard is plastered with sticky notes. Many are half-peeled or scattered across the floor, as if they’ve given up holding on.")
        print("Maybe you should talk to the student?")

    def handle_talk(target):
        # ---- Handle talking to an NPC in the room ----
        if target == "student":
            print("\n👩 The student turns around to face you. Confusion plastered on their face.")
        else:
            print(f"❌There is no {target} here to talk to.")
        if not state["visited"]["computerlab"]:
            print('"Um, is there anything I can help you with?"')
        else:
            print("'It's you again, didn't I help you already?")

    def handle_ask(target):
        if state["visited"]["computerlab"]:
            print("👩'Did you forget the password? It's crypt0.'")
        if target == "student":
            print("👩'Oh, the laptop? Yeah, I know the password, but I need you to solve my riddle first.'")
            print("\nI'm made of only ones and zeros,")
            print("yet I can store music, pictures and prose.")
            print("What am I?")
        else:
            print(f"❌There is no {target} here to ask")

    def handle_answer(response):
        if state["visited"]["computerlab"]:
            print(f"The student looks annoyed and decides to ignore you.")
            return None
        normalized = response.lower().strip()
        if normalized in ["binary", "binary code", "bits"]:
            print("👩'Yeah, that's right! I was curious if you knew.'")
            print("'Anyway, the password to the laptop is: crypt0'")
            print("'Don't forget it!'")
            print(f"You managed to successfully obtain the password.")
            print("It's worth to check out that laptop out.")
            state["visited"]["computerlab"] = True
        else:
            print("The student looks amused.")
            print("👩'Yeah, I think you need to think it over.'")
            print("You return to the corridor in shame.")
            return "corridor"

    def handle_help():
        # ---- Handle help commands ----
        print("\nAvailable commands:")
        print("- look around         : Examine the room and its contents.")
        print("- go corridor / back  : Leave the room and return to the corridor.")
        print("- talk student        : Talk to the student.")
        print("- ask student         : Ask a student a question.")
        print("- answer              : Answer the question.")
        print("- ?                   : Show this help message.")
        print("- quit                : Quit the game entirely.")

    def handle_go(destination):
        # ---- Handle movement out of the room ----
        if destination in ["corridor", "back"]:
            print("You step away from the lively room and return to the corridor.")
            return "corridor"
        else:
            print(f"❌ You can't go to '{destination}' from here.")
            return None
    while True:
        command = input("> ")

        if command == "look around":
            handle_look()

        elif command == "?":
            handle_help()

        elif command.startswith("go "):
            destination = command[3:].strip()
            result = handle_go(destination)
            if result:
                return result

        elif command.startswith("talk "):
            target = command[5:].strip()
            handle_talk(target)

        elif command.startswith("ask "):
            target = command[4:].strip()
            handle_ask(target)

        elif command.startswith("answer "):
            response = command[7:].strip()
            result = handle_answer(response)
            if result:
                return result

        elif command == "quit":
            print("👋 You decide there's nothing for you to do here.")
            sys.exit()

        else:
            print("❓ Unknown command. Type '?' to see available commands.")
