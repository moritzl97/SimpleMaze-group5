# -----------------------------------------------------------------------------
# File: cloudroom.py
# Room: Cloud Room (puzzle + MCQ robot)
# -----------------------------------------------------------------------------

import sys
def cloudroom_enter(state):

    state.setdefault("_cloudroom", {
        "robot_locked": True,
        "password": "CLOUD",
        "quiz_passed": False
    })

    print("\n☁️  You enter the Cloud Room.")
    print("Around the perimeter are techy objects. A quiet robot stands in the center, unpowered.")
    if state["completed"]["cloudroom"]:
        if state["_cloudroom"]["quiz_passed"]:
            print("You’ve already solved this room. You can look around or go back to the corridor.")
        else:
            print("You have been here before, but the robot still awaits the correct answers.")
    print("Type '?' for help.")

    return True

def cloudroom_commands(command, state):
    """
    Handle room-specific commands. Return:
      - True  -> the command was executed successfully
      - False -> not known; main.py will try basic commands
      - "go lab corridor or go back" -> if you want to return and continue the journey
    """
    cr = state.setdefault("_cloudroom", {
        "robot_locked": True,
        "password": "CLOUD",
        "quiz_passed": False
    })

    objects = {
        "desk":       "A tidy desk with scattered AWS notes. A sticky note shows the letter 'C'.",
        "poster":     "A large 'Shared Responsibility Model' poster. A corner is circled: 'L'.",
        "server rack":"Old 1U servers hum quietly. On a label you spot the letter 'O'.",
        "whiteboard": "A network diagram and 'IAM -> Least Privilege'. In the corner: 'U'.",
        "plant":      "A thirsty office plant guarding… the letter 'D' on its pot."
    }

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

    # ---- helpers ----
    def show_help():
        print("\nCloud Room commands:")
        print("  look or look around     (take a gander at the surroundings of the room)")
        print("  inspect <object>        (desk, poster, server rack, whiteboard, plant, robot)")
        print("  unlock <password>       (hint: the letters around spell something)")
        print("  talk robot              (starts quiz if unlocked)")
        print("  go <room>               (handled by global 'go' command)")
        return True

    def look_around():
        print("\nYou see objects around the perimeter:")
        for name in objects.keys():
            print(f"  - {name}")
        print("In the middle stands a robot.")
        return True

    def inspect(obj):
        if obj in objects:
            print("\n" + objects[obj])
        elif obj == "robot":
            if cr["robot_locked"]:
                print("\nA silent robot. A prompt on its chest reads: 'Enter password to unlock.'")
            else:
                print("\nThe robot is online. It awaits your answers.")
        else:
            print("\nThere is no such object here.")
        return True

    def unlock(attempt):
        attempt = (attempt or "").strip().upper()
        if attempt == cr["password"]:
            if cr["robot_locked"]:
                cr["robot_locked"] = False
                print("\n🔓 The robot whirs to life. It's ready to talk.")
            else:
                print("\nThe robot is already unlocked.")
        else:
            print("\n❌ Wrong password. The letters you found might help.")
        return True

    def run_quiz():
        print("\n🤖 Robot: 'Answer three questions. Type a, b, or c.'")
        correct = 0
        for i, item in enumerate(quiz, start=1):
            print(f"\nQ{i}. {item['q']}")
            print(f"   a) {item['opts']['a']}")
            print(f"   b) {item['opts']['b']}")
            print(f"   c) {item['opts']['c']}")
            while True:
                ans = input("Your answer (a/b/c): ").strip().lower()
                if ans in ("a", "b", "c"):
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
        if cr["robot_locked"]:
            print("\nThe robot is locked. Maybe the letters around the room form a password…")
            return True
        if state["_cloudroom"]["quiz_passed"]:
            print("You've already talked to the robot. You can continue on your journey to the next rooms!")
            return True
        finished = run_quiz()
        if finished:
            cr["quiz_passed"] = True
            state["completed"]["cloudroom"] = True
            print("\nYou feel a subtle shift — the room acknowledges your success.")
            print("You can 'go lab corridor' to continue your journey.")
        return True

    # ---- dispatch ----
    if command in ("?", "help"):
        return show_help()

    if command == "look" or command == "look around":
        return look_around()

    if command.startswith("inspect "):
        target = command.replace("inspect", "", 1).strip()
        return inspect(target)

    if command.startswith("unlock"):
        attempt = command.replace("unlock", "", 1).strip()
        return unlock(attempt)

    if command in ("talk robot", "talk to robot"):
        return talk_robot()

    # Not handled here — let basic commands or GO handle it
    return False