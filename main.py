# -----------------------------------------------------------------------------
# File: main.py
# ACS School Project - Simple Maze Example
# Organization: THUAS (The Hague University of Applied Sciences)
# Location: Delft
# Date: July 2025
# -----------------------------------------------------------------------------

from rooms import enterCorridor, enterStudyLandscape, enterClassroom2015, enterProjectRoom3, enterCyberRoom, \
    enterCloudRoom, enterDragonRoom, control_room, enterRiddleroom, enterComputerlab

print("****************************************************************************")
print("*                      Welcome to the School Maze!                         *")
print("*        Your goal is to explore all important rooms in the school.        *")
print("*    You may need to solve challenges to collect items and unlock rooms.   *")
print("*               Once you've visited all rooms, you win!                    *")
print("****************************************************************************")

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

while True:
    current = state["current_room"]

    if current == "corridor":
        state["current_room"] = enterCorridor(state)

    elif current == "studylandscape":
        state["current_room"] = enterStudyLandscape(state)

    elif current == "classroom2015":
        state["current_room"] = enterClassroom2015(state)

    elif current == "projectroom3":
        state["current_room"] = enterProjectRoom3(state)

    elif current == "cyberroom":
        state["current_room"] = enterCyberRoom(state)

    elif current == "cloudroom":
        state["current_room"] = enterCloudRoom(state)

    elif current == "riddleroom":
        state["current_room"] = enterRiddleroom(state)
    elif current == "dragonroom":
        state["current_room"] = enterDragonRoom(state)
    elif current == "controlroom":
        state["current_room"] = control_room(state)
    elif current == "computerlab":
        state["current_room"] = enterComputerlab(state)



    else:
        print("Unknown room. Exiting game.")
        break
