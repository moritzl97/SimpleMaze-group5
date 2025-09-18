# -----------------------------------------------------------------------------
# File: cloudroom.py
# Room: Cloud Room (puzzle + MCQ robot)
# -----------------------------------------------------------------------------

import sys

def enterCloudRoom(state):

    objects = {
        "desk":       "A tidy desk with scattered AWS notes. A sticky note shows the letter 'C'.",
        "poster":     "A large 'Shared Responsibility Model' poster. A corner is circled: 'L'.",
        "server rack":"Old 1U servers hum quietly. On a label you spot the letter 'O'.",
        "whiteboard": "A network diagram and 'IAM -> Least Privilege'. In the corner: 'U'.",
        "plant":      "A thirsty office plant guarding… the letter 'D' on its pot."
    }

    PASSWORD = "CLOUD"

    robot_locked = True

    quiz = [
        {
            "q": "What does AWS stand for?",
            "opts": {"a": "Amazon Web Services", "b": "Advanced Web Systems", "c": "Automated Workload Suite"},
            "ans": "a"
        },
        {
            "q": "Which is an AWS object storage service?",
            "opts": {"a": "EBS", "b": "S3", "c": "EFS"},
            "ans": "b"
        },
        {
            "q": "What best describes an EC2 instance?",
            "opts": {"a": "A managed SQL database", "b": "A serverless function", "c": "A virtual machine in the cloud"},
            "ans": "c"
        }
    ]

    def show_intro():
        print("\n☁️  You enter the Cloud Room.")
        print("Around the perimeter are techy objects. A quiet robot stands in the center, unpowered.")
        if state["visited"]["cloudroom"]:
            print("You’ve already solved this room. You can look around or go back to the corridor.")
        print("Type '?' for help.")

    def help_text():
        print("\nCommands:")
        print("  look                        → list visible things here")
        print("  inspect <object>            → read a description (desk, poster, server rack, whiteboard, plant, robot)")
        print("  unlock <password>           → try to power up the robot")
        print("  talk robot                  → talk to the robot (quiz will start if unlocked)")
        print("  go corridor                 → leave to the corridor")
        print("  quit                        → exit game")

    def look_around():
        print("\nYou see objects around the perimeter:")
        for name in objects.keys():
            print(f"  - {name}")
        print("In the middle stands a robot.")

    def inspect(obj):
        if obj in objects:
            print("\n" + objects[obj])
        elif obj == "robot":
            if robot_locked:
                print("\nA silent robot. A prompt on its chest reads: 'Enter password to unlock.'")
            else:
                print("\nThe robot is online. It awaits your answers")
        else:
            print("\nThere is no such object here.")

    def unlock(attempt):
        nonlocal robot_locked
        if not attempt:
            print("\nUsage: unlock <password>")
            return
        if attempt.strip().upper() == PASSWORD:
            if robot_locked:
                robot_locked = False
                print("\n🔓 Correct password! The robot powers on and looks at you expectantly.")
            else:
                print("\nThe robot is already unlocked.")
        else:
            print("\n❌ Wrong password. The robot remains silent.")

    def run_quiz():
        # Returns True if all answers correct, False otherwise.
        print("\n🤖 Robot: 'Answer three questions. Type a, b, or c.'")
        correct = 0
        for i, item in enumerate(quiz, start=1):
            print(f"\nQ{i}. {item['q']}")
            print(f"   a) {item['opts']['a']}")
            print(f"   b) {item['opts']['b']}")
            print(f"   c) {item['opts']['c']}")
            while True:
                ans = input("Your answer (a/b/c): ").strip().lower()
                if ans in ("a","b","c"):
                    break
                print("Please type a, b, or c.")
            if ans == item["ans"]:
                print("✅ Correct.")
                correct += 1
            else:
                print("❌ Incorrect.")
        if correct == len(quiz):
            print("\n🎉 Robot: 'Well done! You passed.'")
            return True
        else:
            print(f"\nRobot: 'You answered {correct}/{len(quiz)} correctly. Try again when ready.'")
            return False

    def talk_robot():
        if robot_locked:
            print("\nThe robot is locked. Maybe the letters around the room form a password…")
            return False
        # Run quiz; if passed, mark visited and suggest leaving
        passed = run_quiz()
        if passed:
            state["visited"]["cloudroom"] = True
        return passed

    # ---- ROOM LOOP ----
    show_intro()
    while True:
        cmd = input("\n> ").strip().lower()

        if cmd in ("?", "help"):
            help_text()

        elif cmd == "look":
            look_around()

        elif cmd.startswith("inspect "):
            inspect(cmd.replace("inspect", "", 1).strip())

        elif cmd.startswith("unlock"):
            attempt = cmd.replace("unlock", "", 1).strip()
            unlock(attempt)

        elif cmd in ("talk robot", "talk to robot"):
            finished = talk_robot()
            # If solved, send player back (or let them decide)
            if finished:
                print("You can 'go corridor' to continue your journey.")
            # remain in room so they can look/leave themselves

        elif cmd == "go corridor":
            # Leaving is always allowed. Only 'visited' is gated by quiz pass.
            return "corridor"

        elif cmd == "quit":
            print("👋 Goodbye, adventurer.")
            sys.exit(0)

        else:
            print("Unknown command. Type '?' for help.")
