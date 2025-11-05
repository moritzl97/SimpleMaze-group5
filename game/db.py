# db.py
import json
from game.utils import resource_path

def init_db(state):
    conn = state["db_conn"]
    cursor = conn.cursor()
    #--------------Create common tables----------------#
    # create table that stores player name
    conn.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    player_name TEXT UNIQUE NOT NULL
                    );""")
    # create table containing all items
    conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL
                    );""")
    # create table that the save_id that identifies a save file and all relevant values
    conn.execute("""
                CREATE TABLE IF NOT EXISTS saves (
                    save_id INTEGER PRIMARY KEY,
                    player_id INTEGER NOT NULL,
                    current_room TEXT,
                    previous_room TEXT,
                    elapsed_time REAL DEFAULT 0,
                    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    game_finished BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (player_id) REFERENCES players(player_id)
                    );""")
    # create table to store inventory
    conn.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    save_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL,
                    PRIMARY KEY (save_id, item_id),
                    FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                    FOREIGN KEY (item_id) REFERENCES items(item_id)
                    );""")
    # create table that store miscellaneous flags
    conn.execute("""
                CREATE TABLE IF NOT EXISTS flags (
                    flag_id TEXT PRIMARY KEY
                    );""")
    # create table to connect miscellaneous flags to save id
    conn.execute("""
                CREATE TABLE IF NOT EXISTS flag_status (
                    save_id INTEGER NOT NULL,
                    flag_id TEXT NOT NULL,
                    status BOOLEAN DEFAULT FALSE,
                    PRIMARY KEY (save_id, flag_id),
                    FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                    FOREIGN KEY (flag_id) REFERENCES flags(flag_id)
                    );""")
    # create table to store all room names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        );
    """)
    # create table that store room entered and completed status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS save_rooms (
            save_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            entered BOOLEAN DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            PRIMARY KEY (save_id, room_id),
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        );
    """)
    # create table that stores all achievement names and icons
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS achievements (
                    achievement_id TEXT PRIMARY KEY,
                    name TEXT UNIQUE,
                    icon TEXT
                   );""")
    # create table that relates the gained achievements to a save id
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS savefile_to_achievement (
                    save_id INTEGER NOT NULL,
                    achievement_id TEXT NOT NULL,
                    PRIMARY KEY (save_id, achievement_id),
                    FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                    FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id)
                   );""")
    #--------------end create common tables----------------#

    # --------------Create room specific tables------------#
    # Computer Lab tables

    conn.execute("""
                 CREATE TABLE IF NOT EXISTS computer_lab_state (
                     save_id           INTEGER PRIMARY KEY,
                     riddle_answer     INTEGER DEFAULT 0,
                     laptop_unlocked   INTEGER DEFAULT 0,
                     laptop_softlocked REAL    DEFAULT 0,
                     FOREIGN KEY (save_id) REFERENCES saves (save_id) ON DELETE CASCADE
                 );
                 """)

    conn.execute("""
                 CREATE TABLE IF NOT EXISTS computer_lab_seminars (
                     save_id      INTEGER NOT NULL,
                     seminar_name TEXT    NOT NULL,
                     completed    INTEGER DEFAULT 0,
                     PRIMARY KEY (save_id, seminar_name),
                     FOREIGN KEY (save_id) REFERENCES saves (save_id) ON DELETE CASCADE
                 );
                 """)

    # CyberRoom tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cyber_room_state (
            save_id        INTEGER PRIMARY KEY,
            code_unlocked  INTEGER DEFAULT 0,
            completed      INTEGER DEFAULT 0,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cyber_room_panels (
            save_id   INTEGER NOT NULL,
            panel_id  TEXT    NOT NULL,
            solved    INTEGER DEFAULT 0,
            PRIMARY KEY (save_id, panel_id),
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        );
    """)
    # Library
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS library_books (
                     book_id INTEGER PRIMARY KEY,
                     title TEXT UNIQUE 
                 );
                 """)
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS library_state (
                     save_id INTEGER NOT NULL,
                     book_id INTEGER NOT NULL,
                     PRIMARY KEY (save_id, book_id),
                     FOREIGN KEY (save_id) REFERENCES saves (save_id) ON DELETE CASCADE
                 );
                 """)

    #Cloud room table for state saving
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cloud_room_state (
            save_id       INTEGER PRIMARY KEY,
            robot_locked  INTEGER DEFAULT 1,
            quiz_passed   INTEGER DEFAULT 0,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        );
    """)

    #dragon room tables
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_objects (
                     object_id INTEGER PRIMARY KEY,
                     name TEXT UNIQUE,
                     dialog_tree TEXT
                 );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_npcs (
                     npc_id INTEGER PRIMARY KEY,
                     name TEXT UNIQUE,
                     dialog_tree TEXT
                 );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_trades (
                     trade_id INTEGER PRIMARY KEY,
                     sale_item INTEGER UNIQUE,
                     wanted_item INTEGER,
                     CONSTRAINT fk_sale FOREIGN KEY (sale_item) REFERENCES items(item_id),
                     CONSTRAINT fk_item FOREIGN KEY (wanted_item) REFERENCES items(item_id)
                       );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_current_objects (
                     save_id INTEGER,
                     object_id INTEGER,
                     current_chapter TEXT DEFAULT 'first_chapter',
                     current_node TEXT DEFAULT 'start',
                     PRIMARY KEY (save_id, object_id),
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                     CONSTRAINT fk_object FOREIGN KEY (object_id) REFERENCES dragon_room_objects(object_id)
                 );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_current_npcs (
                     save_id INTEGER,
                     npc_id INTEGER,
                     current_chapter TEXT DEFAULT 'first_chapter',
                     current_node TEXT DEFAULT 'start',
                     PRIMARY KEY (save_id, npc_id),
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                     CONSTRAINT fk_npc FOREIGN KEY (npc_id) REFERENCES dragon_room_npcs(npc_id)
                 );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_current_items (
                     save_id INTEGER,
                     item_id INTEGER,
                     PRIMARY KEY (save_id, item_id),
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                     CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES items(item_id)
                   );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_current_trades (
                     save_id INTEGER,
                     trade_id INTEGER,
                     PRIMARY KEY (save_id, trade_id),
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
                     CONSTRAINT fk_trade FOREIGN KEY (trade_id) REFERENCES dragon_room_trades(trade_id)
                       );""")
    #--------------Create room specific tables end------------#
    conn.commit()

    #--------------Insert values into common tables-----------#
    # insert room names
    all_rooms = [
        "cloud_room", "computer_lab", "control_room", "cyber_room", "dragon_room",
        "riddle_room", "roof_garden", "library", "study_landscape",
        "e_w_corridor", "lab_corridor", "n_s_corridor"
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO rooms (name, description) VALUES (?, ?);",
        [(room, "") for room in all_rooms]
    )
    # insert all possible items
    insert_query = "INSERT OR IGNORE INTO items (name) VALUES (?);"
    rows_to_insert = [
        #dragon room
        ('lockpick',),('broadsword',),('sneaking_boots',),('chalk',),('paper',),('invisibility_cloak',),('milk_carton',),('gemstone',),('pickaxe',),('cursed_trophy',),
        #cloud_room
        ('cursed_robot_head',),
        #cyberroom
        ('?_key',),
        #riddleroom
        ('cursed_magnet',),('money',),
        #computer lab
        ('cloud_key',),
        #study landscape
        ('rusty_key',),('lab_permit',),
        # library
        ('python_tutorial',),
        # roof garden
        ('cursed_rose',),
        # tbd
        ('beer',),
        #controlroom
        ('bottle_opener',),
    ]
    cursor.executemany(insert_query, rows_to_insert)
    # insert books for library
    insert_query = "INSERT OR IGNORE INTO library_books (title) VALUES (?);"
    rows_to_insert = [
        ('intercultural sensitivity',),('beginner sql',),('python tutorial',),
    ]
    cursor.executemany(insert_query, rows_to_insert)
    # insert miscellaneous flags
    insert_query = "INSERT OR IGNORE INTO flags (flag_id) VALUES (?);"
    rows_to_insert = [
        # dragon room
        ('n_s_unlocked',),
        ('tutorial_finished',),
        ('skip_tutorial',),
        ('challenge_solved',),
        ('side_quest_completed',),
    ]
    cursor.executemany(insert_query, rows_to_insert)
    # insert all possible achievements
    insert_query = "INSERT OR IGNORE INTO achievements (achievement_id, name, icon) VALUES (?, ?, ?);"
    rows_to_insert = [
        # general
        ('finish_a_game', 'Finish a game', '🏅',),
        # computer lab
        ('gnomed', 'You have been gnomed!', '🍄'),
        # dragon room
        ('kill_dragon', 'Kill the dragon', '🗡️🐉',),
        ('bribe_dragon', 'Bribe the dragon', '💎',),
        ('steal_trophy', 'Steal the trophy', '🥷🏆',),
        ('destroy_chest', 'Hopefully nothing important was in there...', '💥📦',),
        # roof garden
        ('pet_cat', 'Pet a black cat','🐈‍⬛',),
        #study landscape
        ('coffee_adict', 'Being addicted to coffee', '☕️',),
        #cyberroom
        ('schoolnerd', 'Go back to school', '📓',),
        #riddleroom
        ('einstein', 'Solved on first attempt', '🤓',),
        ('jackpot', 'Win a Jackpot', '🎰',),
        #cyberroom
        ('ghost_release', 'Released the ghost', '👻',),
        ('ghost_lock', 'Locked the ghost in the room', '☠️'),
        # controlroom
        ('robot_master', 'Gained the robot’s respect', '🤖',),


    ]
    cursor.executemany(insert_query, rows_to_insert)
    #--------------End insert values into common tables-----------#

    #--------------Insert values into room specific tables--------#
    asset_file_path = resource_path("assets/dragon_room_dialog.json")
    #dragon room insert data in tables
    with open(asset_file_path, "r", encoding="utf-8") as file:
        dialog_tree = json.load(file)
    # dragon room insert all possible objects
    insert_query = "INSERT OR IGNORE INTO dragon_room_objects (name, dialog_tree) VALUES (?, ?);"
    rows_to_insert = [
        ('cracked_wall', json.dumps(dialog_tree['dialogue_tree_cracked_wall'])),
        ('blackboard', json.dumps(dialog_tree['dialogue_tree_blackboard'])),
        ('desk', json.dumps(dialog_tree['dialogue_tree_desk'])),
        ('chest', json.dumps(dialog_tree['dialogue_tree_chest'])),
        ('hole', json.dumps(dialog_tree['dialogue_tree_hole'])),
    ]
    cursor.executemany(insert_query, rows_to_insert)
    # dragon room insert all possible npcs
    insert_query = "INSERT OR IGNORE INTO dragon_room_npcs (name, dialog_tree) VALUES (?, ?);"
    rows_to_insert = [
        ('fairy', json.dumps(dialog_tree['dialogue_tree_fairy'])),
        ('kobold', json.dumps(dialog_tree['dialogue_tree_kobold'])),
        ('dragon', json.dumps(dialog_tree['dialogue_tree_dragon'])),
        ('shopkeeper', '')
    ]
    cursor.executemany(insert_query, rows_to_insert)
    # dragon room insert all possible trades
    cursor.execute("""
        INSERT OR IGNORE INTO dragon_room_trades (sale_item, wanted_item)
        SELECT sale.item_id, wanted.item_id
        FROM (SELECT name, item_id FROM items) AS sale
        JOIN (SELECT name, item_id FROM items) AS wanted
        WHERE sale.name = 'gemstone' AND wanted.name = 'broadsword'
            OR sale.name = 'chalk' AND wanted.name = 'sneaking_boots'
            OR sale.name = 'pickaxe' AND wanted.name = 'lockpick';
                    """)
    #--------------End of Insert values into room specific tables------#

    # db setup finished
    conn.commit()
    return

def create_new_save(state, current_player_name):
    # create a new save file
    conn = state["db_conn"]
    cursor = conn.cursor()

    # Try insert the player into players if they have not played the game yet
    cursor.execute("INSERT OR IGNORE INTO players (player_name) VALUES (?)", (current_player_name,))
    # Fetch the player id
    cursor.execute("SELECT player_id FROM players WHERE player_name = ?", (current_player_name,))
    player_id = cursor.fetchone()[0]

    # Create a new entry in the saves table (representing a save file) with a unique save id
    cursor.execute("INSERT INTO saves (player_id, current_room, previous_room) VALUES (?,?,?)", (player_id,"study_landscape","study_landscape"))
    save_id = cursor.lastrowid
    state["save_id"] = save_id

    # --- Initialize per-room flags ---
    cursor.execute("SELECT room_id FROM rooms;")
    all_room_ids = [r[0] for r in cursor.fetchall()]
    for room_id in all_room_ids:
        entered = 1 if room_id == 9 else 0  # assuming 'study_landscape' inserted 9th
        cursor.execute("""
            INSERT INTO save_rooms (save_id, room_id, entered, completed)
            VALUES (?, ?, ?, 0);
        """, (save_id, room_id, entered))

    # miscellaneous flags
    cursor.execute("""
            INSERT INTO flag_status (save_id, flag_id, status)
            SELECT ?, flag_id, FALSE
            FROM flags;
            """, (save_id,))

    # initialise cloud_room table
    cursor.execute("""
        INSERT INTO cloud_room_state (save_id, robot_locked, quiz_passed)
        VALUES (?, 1, 0);
    """, (save_id,))
    #library
    cursor.execute("""
            INSERT INTO library_state (save_id, book_id)
            SELECT ?, book_id
            FROM library_books;
            """, (save_id,))

    #dragon room
    # insert starting objects in the room
    current_object_names = ('cracked_wall', 'blackboard', 'desk', 'chest', 'hole',)
    placeholders = ','.join(['?'] * len(current_object_names))
    insert_query = f"""
            INSERT INTO dragon_room_current_objects (save_id, object_id)
            SELECT ?, object_id
            FROM dragon_room_objects
            WHERE name IN ({placeholders});
    """
    cursor.execute(insert_query, (save_id, *current_object_names))
    # insert starting items in the room
    current_item_names = ('pickaxe',)
    placeholders = ','.join(['?'] * len(current_item_names))
    insert_query = f"""
            INSERT INTO dragon_room_current_items (save_id, item_id)
            SELECT ?, item_id
            FROM items
            WHERE name IN ({placeholders});
        """
    cursor.execute(insert_query, (save_id, *current_item_names))
    # insert starting trades
    cursor.execute("""
            INSERT INTO dragon_room_current_trades (save_id, trade_id)
            SELECT ?, trade_id
            FROM dragon_room_trades;
            """, (save_id,))

    conn.commit()
    return

def list_saves(conn):
    # list all saves that are not finished
    return conn.execute("""
            SELECT s.save_id, p.player_name, s.current_room, s.saved_at
            FROM saves s
            JOIN players p ON s.player_id = p.player_id
            WHERE s.game_finished = False
            ORDER BY s.saved_at DESC;
        """).fetchall()

def delete_save(state, save_id):
    #delete a save file for a given save id
    conn = state["db_conn"]
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saves WHERE save_id = ?;", (save_id,))
    conn.commit()
    print("Save deleted.")