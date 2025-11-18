# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

# All commands that are available in all rooms are stored here
import time
from game.utils import *
from game.db_utils import *
from game.screens import scoreboard_menu, handle_quit
import datetime

def handle_go(command, state, room_functions, room_exits):
    # lets the player go in another room
    if command.startswith("go "):
        destination_room = None
        input_destination_room = command[3:]
        if input_destination_room == "back":
            destination_room = db_get_previous_room(state)
        else:
            input_destination_room = input_destination_room.replace(" ", "").replace("-", "").replace("_", "")
            room_aliases = {"nscor":"nscorridor",
                            "northsouthcorridor":"nscorridor",
                            "northsouthcor": "nscorridor",
                            "ewcor":"ewcorridor",
                            "eastwestcorridor": "ewcorridor",
                            "eastwestcor": "ewcorridor",
                            "labcor":"labcorridor",
                            }

            input_destination_room = room_aliases.get(input_destination_room, input_destination_room)

            for room in room_exits.keys():
                if room.replace("_", "") == input_destination_room:
                    destination_room = room
                    break

        current_room = db_get_current_room(state)

        if destination_room in room_exits.get(current_room, []):
            clear_screen()
            destination_room_display_name = destination_room.replace("_", " ").title()
            print(f"You walk toward the door to {destination_room_display_name}.")
            print_room_entry_banner(destination_room_display_name)

            entry_allowed = room_functions[destination_room]["enter_function"](state)

            if entry_allowed:
                db_mark_room_entered(state, destination_room)
                db_set_current_room(state, destination_room)
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

    clear_screen()

    print_room_entry_banner(destination_room)

    entry_allowed = room_functions[destination_room]["enter_function"](state)

    if not entry_allowed:
        print("WARNING: This room would currently not be accessible to the player. This command still lets you enter. However this could break things down the line.")
    db_mark_room_entered(state, destination_room)
    db_set_current_room(state, destination_room)
    return True

def handle_admin_give(command, state):
    item = command[11:]
    db_add_item_to_inventory(state, item)
    if db_is_item_in_inventory(state, item):
        print("Admin command executed. Item was added to inventory.")
        print("WARNING: This could break things down the line.")
    else:
        print("Item not found.")
    return

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

def show_inventory(state):
    #list items in inventory
    item_list = db_get_all_items_in_inventory(state)
    if item_list:
        print("You are carrying:")
        for item in item_list:
            print(f" - {item.replace('_', ' ').title()}")
    else:
        print("You are not carrying anything.")

def show_status(state):
    completed_list = db_get_completed_status_of_all_rooms(state)
    visited_rooms = sum(1 for v in completed_list if v)
    total_rooms = len(completed_list)
    percentage = int((visited_rooms / total_rooms) * 100)
    player_name = db_get_player_name(state)
    elapsed_seconds = int(time.time() - state["start_time"])

    time_delta = datetime.timedelta(seconds=elapsed_seconds)
    total_seconds = int(time_delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time_formatted = f"{hours}:{minutes:02}:{seconds:02}"

    print("#" + "-"* 124 + "#")
    all_items = db_get_all_items_in_inventory(state)
    cursed_items = [item.replace("_"," ").title() for item in all_items if item.startswith("cursed")]
    print_and_center(f"Progress of {player_name}")
    print_and_center(f"{visited_rooms}/{total_rooms} Rooms completed ({percentage}%), {len(cursed_items)}/4 Cursed items, Time: {time_formatted}")
    completed_rooms = db_get_completed_rooms_list(state)
    completed_rooms = [item.replace("_"," ").title() for item in completed_rooms]
    achievements = db_get_all_achievements_of_a_save(state, state["save_id"])
    if completed_rooms:
        print(f"Completed Rooms: {Color.green + ', '.join(completed_rooms) + Color.end}")
    if cursed_items:
        print(f"Cursed Items: {Color.purple + ', '.join(cursed_items) + Color.end}")
    if achievements:
        print(f"Earned Achievements: {' '.join(achievements)}")
    print("#" + "-"* 124 + "#")

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
        self.map_str = """+---------+------------+-------------+---------+----------+---------+---------+----------+
|         |            |             |         |          |         |         |          |
|         |            |             |         |          |         |         |          |
|         |            |             #         |          |         +----+-##-+          |
|         |            |             |         |          |         |    #    |          |
|         |            |             +---------+-------##-+------##-+----+    #          |
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
                      MapRoom("study_landscape", 3*91+26, 576, ["Study","Landscape"]),
                      MapRoom("e_w_corridor", 6*91+50, 590, ["E W Corridor"]),
                      MapRoom("lab_corridor", 7*91+12, 658, ["Lab Cor"]),
                      MapRoom("n_s_corridor", 6*91+76, 440, ["N","S"," ","C","o","r"]),
                      MapRoom("library",2*91+39,3*91+42,["Library"]),
                      MapRoom("roof_garden", 2*91+50, 416, ["Roof","Garden"]),
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
            if db_get_room_completed(state, room.name):
                color = Color.green
            elif db_get_room_entered(state, room.name):
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
    current_room = db_get_current_room(state)

    floor_map = Map()
    floor_map.show(current_room, state, room_exits)

def handle_basic_commands(command, state, room_exits):
    if command in ["quit", "exit", "exit game", "quit game"]:
        quit_flag = handle_quit(state)
        return quit_flag
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
    elif command == "scoreboard":
        scoreboard_menu(state, 5)
        return True
    elif command.startswith("admin give "):
        handle_admin_give(command, state)
        return True
    return False