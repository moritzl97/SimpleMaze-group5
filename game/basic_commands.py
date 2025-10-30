# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

# All commands that are available in all rooms are stored here
import time
import math
from game.utils import *
import sqlite3
from game.db_utils import *
import datetime

def handle_pause(state):

    paused = True
    state["elapsed_time"] = time.time() - state["start_time"]
    #player_name = state["player_name"]
    #save_state(player_name, state)
    print(r"""
                _______  _______           _______  _______ 
                (  ____ )(  ___  )|\     /|(  ____ \(  ____ \
                | (    )|| (   ) || )   ( || (    \/| (    \/
                | (____)|| (___) || |   | || (_____ | (__    
                |  _____)|  ___  || |   | |(_____  )|  __)   
                | (      | (   ) || |   | |      ) || (      
                | )      | )   ( || (___) |/\____) || (____/\
                |/       |/     \|(_______)\_______)(_______/
    """)
    print("You can type 'time', 'resume', or 'quit'.")

    while True:
        command = input("> ").strip().lower()

        if command == "time":
            display_time(state, paused)

        elif command == "resume":
            handle_resume(state, paused)
            break

        elif command == "quit":
            quit_flag = handle_quit(state)
            return quit_flag

        else:
            print("Game is paused. Only available commands: time, resume and quit.")

def handle_resume(state, paused):

    state["start_time"] = time.time() - state["elapsed_time"]
    paused = False
    print("Game resumed.")

def display_time(state, paused):

    if paused:
        elapsed = state["elapsed_time"]
    else:
        elapsed = time.time() - state["start_time"]

    print(f"Elapsed time: {int(elapsed)} seconds")

def handle_go(command, state, room_functions, room_exits):
    if command.startswith("go "):
        destination_room = None
        input_destination_room = command[3:]
        if input_destination_room == "back":
            destination_room = state["previous_room"][:]
        else:
            input_destination_room = input_destination_room.replace(" ", "").replace("-", "").replace("_", "")
            room_aliases = {"nscor":"nscorridor",
                            "northsouthcorridor":"nscorridor",
                            "northsouthcor": "nscorridor",
                            "ewcor":"ewcorridor",
                            "eastwestcorridor": "ewcorridor",
                            "eastwestcor": "ewcorridor",
                            "labcor":"labcorridor",
                            "pr3":"projectroom3",
                            "projectroom": "projectroom3",
                            "class2015":"classroom2015",
                            "class":"classroom2015",
                            "classroom":"classroom2015"}

            input_destination_room = room_aliases.get(input_destination_room, input_destination_room)

            for room in room_exits.keys():
                if room.replace("_", "") == input_destination_room:
                    destination_room = room
                    break

        current_room = state["current_room"]

        if destination_room in room_exits.get(current_room, []):
            clear_screen()
            destination_room_display_name = destination_room.replace("_", " ").title()
            print(f"You walk toward the door to {destination_room_display_name}.")
            print_room_entry_banner(destination_room_display_name)

            entry_allowed = room_functions[destination_room]["enter_function"](state)

            if entry_allowed:
                state["entered"][destination_room] = True
                state["previous_room"] = state["current_room"]
                state["current_room"] = destination_room
            else:
                print_room_entry_banner(current_room)
        else:
            print(f"❌ You can't go to '{input_destination_room}' from here.")
        return True
    else:
        return False

def handle_admin_go(command, state, room_functions, room_exits):
    destination_room = None
    input_destination_room = command[9:]

    input_destination_room = input_destination_room.replace(" ", "").replace("-", "").replace("_", "")
    for room in room_functions.keys():
        if room.replace("_", "") == input_destination_room:
            destination_room = room
            break

    if destination_room is None:
        print(f"The room {input_destination_room} doesn't exist")
        return False

    current_room = state["current_room"]

    clear_screen()

    print_room_entry_banner(destination_room)

    entry_allowed = room_functions[destination_room]["enter_function"](state)

    if entry_allowed:
        state["entered"][destination_room] = True
        state["previous_room"] = room_exits[destination_room][0]
        state["current_room"] = destination_room
    else:
        print_room_entry_banner(current_room)
    return True


    destination_room = command[9:].replace(" ", "_").replace("-", "_")

    current_room = state["current_room"]

    print(f"You walk toward the door to {destination_room}.")
    entry_allowed = room_functions[destination_room]["enter_function"](state)

    if entry_allowed:
        state["previous_room"] = state["current_room"]
        state["current_room"] = destination_room

    else:
        print(f"You can't enter right now.")
    return True

def handle_help():
    #Show help message with available commands.
    print("\nAvailable commands:")
    print("- go <room>           : Go to the entered room.")
    print("- go back             : Return to the room you came from.")
    print("- map                 : Show the map and all exits.")
    print("- inventory           : Show all items in your inventory.")
    print("- ?                   : Show this help message.")
    print("- status              : Show the progress of the game.")
    print("- scoreboard          : Show leaderboard of the top 5 players")
    print("- pause               : Pause the game")
    print("- quit                : Save and quit to the main menu.")

def handle_quit(state):
    clear_screen()
    save_entry_to_scoreboard(state)
    # TODO save time
    print("Game Saved".center(82))
    print("\n")
    print("You wake up from a nightmare. Was this all a dream?".center(82))
    time.sleep(3)
    return "quit"

def show_inventory(state):
    #list items in inventory
    item_list = db_get_all_items_in_inventory(state)
    if item_list:
        print("You are carrying:")
        for item in item_list:
            print(f" - {item.replace("_"," ").title()}")
    else:
        print("You are not carrying anything.")

def show_status(state):
    visited_rooms = sum(1 for v in state["completed"].values() if v)
    total_rooms = len(state["completed"])
    percentage = int((visited_rooms / total_rooms) * 100)
    player_name = db_get_player_name(state)
    elapsed_seconds = int(time.time() - state["start_time"])
    time_format = datetime.timedelta(seconds=elapsed_seconds)

    print("-" * 70)
    print(f"Progress for {player_name}: {visited_rooms}/{total_rooms} rooms completed ({percentage}%) time: {time_format}")
    completed_rooms = [key.replace("_"," ").title() for key, value in state["completed"].items() if value]
    print(f"Completed rooms: {", ".join(completed_rooms)}")
    print("-" * 70)

def save_entry_to_scoreboard(state):
    visited_rooms = sum(1 for v in state["completed"].values() if v)
    total_rooms = len(state["completed"])
    percentage = int((visited_rooms / total_rooms) * 100)
    nickname = state.get("player_name", "Player")
    elapsed_time = int(time.time() - state["start_time"])
    conn = sqlite3.connect("saves.db")
    conn.execute("""
                 INSERT INTO scoreboard (player_name, percentage, time)
                 VALUES (?, ?, ?) ON CONFLICT(player_name) DO
                 UPDATE SET
                     percentage = excluded.percentage,
                     time = excluded.time;
                 """, (nickname, percentage, elapsed_time))
    conn.commit()

def display_scoreboard(state=None):
    if state:
        save_entry_to_scoreboard(state)
    conn = sqlite3.connect("saves.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scoreboard")
    rows = cursor.fetchall()
    sorted_data = sorted(rows, key=lambda x: (-x[1], x[2]))
    print("🏆 Scoreboard:")
    print("-" * 70)
    for index, row in enumerate(sorted_data):
        print(f"{row[0]}: \t {row[1]}% completed \t {row[2]}s")
        if index == 4:
            break
    print("-" * 70)

class MapRoom:
    def __init__(self, name, text_position, player_position, display_text):
        self.name = name
        self.text_position = text_position
        self.display_text = display_text
        self.player_position = player_position
        self.entered = False
        self.completed = False

class Map:
    def __init__(self):
        self.map_str = """+---------+------------+-------------+--------+----------+----------+---------+----------+
|         |            |             |        |          |          |         |          |
|         |            |             |        |          |          |         |          |
|         |            |             |        |          |          +----+-##-+          |
|         |            |             |        |          |          |    #    |          |
|         |            |             +----##--+-------##-+-------##-+----+    #          |
|         +-------##---+             #                                   #    |          |
|         #            #            +--------##-+-##-+-##-+-##-+-##-+-##-+    +----------+
|         +------------+-#-+-#-+    |           |    |    |    |    |    |    |          |
|         |            |   |   |    |           |    |    |    |    |    |    |          |
|         |            |   |   |    |           |    |    |    |    |    |    #          |
+---------+            +---+---+-##-+-----------+----+----+----+----+----+    |          |
                               |    |                                    +----+----------+"""
        self.map_line_len = 91
        self.rooms = [
                      MapRoom("cloud_room", 4*91+3, 733, ["Cloud","Room"]),
                      MapRoom("computer_lab", 2*91+13, 381, ["Computer","Lab"]),
                      MapRoom("control_room", 9*91+39, 770, ["Control","Room"]),
                      MapRoom("cyber_room", 1*91+71, 258, ["Cyber","Room"]),
                      MapRoom("dragon_room", 9*91+81, 1085, ["Dragon","Room"]),
                      MapRoom("riddle_room", 2*91+81, 538, ["Riddle","Room"]),
                      MapRoom("classroom_2015", 2*91+49, 416, ["Class","2015"]),
                      MapRoom("project_room_3", 10*91+28, 848, ["PR3"]),
                      MapRoom("study_landscape", 3*91+26, 576, ["Study","Landscape"]),
                      MapRoom("e_w_corridor", 6*91+50, 590, ["E-W-Corridor"]),
                      MapRoom("lab_corridor", 7*91+12, 658, ["Lab Cor"]),
                      MapRoom("n_s_corridor", 6*91+76, 440, ["N","S"," ","C","o","r"]),
                      ]
        # Lookup dictionary
        self.room_lookup = {room.name: room for room in self.rooms}

    def _abs_to_line_col(self, abs_pos):
        line = abs_pos // self.map_line_len
        col = abs_pos % self.map_line_len
        return line, col

    def show(self, current_room, state, room_exits):
        # Split original map into lines (keep newline endings)
        lines = self.map_str.splitlines(keepends=True)  # preserves '\n' so indices align with abs positions

        # Collect replacements per line as (col, length_of_target, replacement_string)
        # We'll store (col, replacement_str) but need to sort descending by col when applying.
        replacements = {}  # line_index -> list of (col, target_len, replacement_text)

        # Add room name replacements (colored)
        for room in self.rooms:
            color = ""
            if state["completed"].get(room.name, False):
                color = Color.green
            elif state["entered"][room.name]:
                color = Color.gray

            base_line, base_col = self._abs_to_line_col(room.text_position)

            for i, text in enumerate(room.display_text):
                line_idx = base_line + i
                col_idx = base_col
                colored = color + text + Color.end
                replacements.setdefault(line_idx, []).append((col_idx, len(text), colored))

        # Add player 'X' marker
        room_obj = self.room_lookup.get(current_room)
        line_idx, col_idx = self._abs_to_line_col(room_obj.player_position)
        colored_x = Color.yellow + "X" + Color.end
        replacements.setdefault(line_idx, []).append((col_idx, 1, colored_x))

        # Apply replacements per line, from right to left (descending column) so indexes remain valid
        for line_idx, repls in replacements.items():
            # filter valid replacements within the line length
            orig_line = lines[line_idx]
            # sort by column descending
            for col, target_len, repl_text in sorted(repls, key=lambda x: x[0], reverse=True):
                if col < 0 or col >= len(orig_line):
                    continue
                # split original line into three pieces and replace target slice
                before = orig_line[:col]
                after = orig_line[col + target_len:]
                orig_line = before + repl_text + after
            lines[line_idx] = orig_line

        # Build final map and print
        final_map = "".join(lines)
        print(final_map)
        print(f"Legend: unvisited room, {Color.gray}visited room{Color.end}, {Color.green}completed room{Color.end}, player position {Color.yellow}X{Color.end}")
        print(f"Possible exits: {', '.join(room_exits[current_room]).replace('_', ' ').title()}")


def show_map(state, room_exits):
    current_room = state["current_room"]

    floor_map = Map()
    floor_map.show(current_room, state, room_exits)

def handle_basic_commands(command, state, room_exits):
    if command == "quit":
        quit_flag = handle_quit(state)
        return quit_flag
    elif command == "pause":
        quit_flag = handle_pause(state)
        if quit_flag:
            return quit_flag
        return True
    elif command == "map":
        show_map(state, room_exits)
        return True
    elif command == "status":
        show_status(state)
        return True
    elif command == "help" or command == "?":
        handle_help()
        return True
    elif command == "inventory" or command == "inv":
        show_inventory(state)
        return True
    elif command == "time":
        display_time(state, paused=False)
        return True
    elif command == "scoreboard":
        display_scoreboard(state)
        return True


    return False