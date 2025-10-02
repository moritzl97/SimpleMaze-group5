# -----------------------------------------------------------------------------
# File: main.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

import time

from rooms import enterCorridor, enterStudyLandscape, enterClassroom2015, enterProjectRoom3, enterCyberRoom, \
    enterCloudRoom, enterDragonRoom, control_room, enterRiddleroom, enterComputerlab

print("****************************************************************************")
print("*                      Welcome to the School Maze!                         *")
print("*        Your goal is to explore all important rooms in the school.        *")
print("*    You may need to solve challenges to collect items and unlock rooms.   *")
print("*               Once you've visited all rooms, you win!                    *")
print("****************************************************************************")


# ----------------------------------------------------------------------
# Progress Helper
# ----------------------------------------------------------------------
def show_progress(state):
    visited_rooms = sum(1 for v in state["visited"].values() if v)
    total_rooms = len(state["visited"])
    percentage = (visited_rooms / total_rooms) * 100
    print(f"\n📊 Progress: {visited_rooms}/{total_rooms} rooms visited ({percentage:.1f}%)")
    print("-" * 70)


# ----------------------------------------------------------------------
# Game State
# ----------------------------------------------------------------------
state = {
    "current_room": "corridor",
    "previous_room": "corridor",
    "visited": {
        "classroom2015": False,
        "projectroom3": False,
        "cloudroom": False,
        "cyberroom": False,
        "dragonroom": False,
        "computerlab": False,
        "riddleroom": False,
        "controlroom": False
    },
    "inventory": []
}

state["time"] = time.time()


# ----------------------------------------------------------------------
# Game Loop
# ----------------------------------------------------------------------
while True:
    current = state["current_room"]

    if current == "corridor":
        state["current_room"] = enterCorridor(state)

    elif current == "studylandscape":
        state["current_room"] = enterStudyLandscape(state)

    elif current == "classroom2015":
        state["visited"]["classroom2015"] = True
        state["current_room"] = enterClassroom2015(state)

    elif current == "projectroom3":
        state["visited"]["projectroom3"] = True
        state["current_room"] = enterProjectRoom3(state)

    elif current == "cyberroom":
        state["visited"]["cyberroom"] = True
        state["current_room"] = enterCyberRoom(state)

    elif current == "cloudroom":
        state["visited"]["cloudroom"] = True
        state["current_room"] = enterCloudRoom(state)

    elif current == "riddleroom":
        state["visited"]["riddleroom"] = True
        state["current_room"] = enterRiddleroom(state)

    elif current == "dragonroom":
        state["visited"]["dragonroom"] = True
        state["current_room"] = enterDragonRoom(state)

    elif current == "controlroom":
        state["visited"]["controlroom"] = True
        state["current_room"] = control_room(state)

    elif current == "computerlab":
        state["visited"]["computerlab"] = True
        state["current_room"] = enterComputerlab(state)

    else:
        print("Unknown room. Exiting game.")
        break

    # Show progress after each move
    show_progress(state)

    # Win condition
    if all(state["visited"].values()):
        print("\n🎉 Congratulations! You've visited all the rooms and completed the maze! 🎉")
        break
