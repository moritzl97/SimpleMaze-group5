# db.py
import sqlite3, json, datetime

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"
def now_iso(): return datetime.datetime.now(datetime.UTC).strftime(ISO)

def init_db(state):
    conn = state["db_conn"]

    # conn.execute("""
    #   CREATE TABLE IF NOT EXISTS saves (
    #     player_name   TEXT PRIMARY KEY,
    #     state_json    TEXT NOT NULL,
    #     current_room  TEXT NOT NULL,
    #     created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    #     updated_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
    #   );
    # """)
    # conn.execute("CREATE INDEX IF NOT EXISTS idx_saves_updated_at ON saves(updated_at DESC);")
    # conn.commit()



    cursor = conn.cursor()
    # Create common tables
    conn.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    player_name TEXT UNIQUE NOT NULL
                    );""")
    conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    item_id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL
                    );""")
    conn.execute("""
                CREATE TABLE IF NOT EXISTS saves (
                    save_id INTEGER PRIMARY KEY,
                    player_id INTEGER NOT NULL,
                    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (player_id) REFERENCES players(player_id)
                    );""")
    conn.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    save_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL,
                    PRIMARY KEY (save_id, item_id),
                    FOREIGN KEY (save_id) REFERENCES saves(save_id),
                    FOREIGN KEY (item_id) REFERENCES items(item_id)
                    );""")
    conn.execute("""
                CREATE TABLE IF NOT EXISTS flags (
                    flag_id TEXT PRIMARY KEY
                    );""")
    conn.execute("""
                CREATE TABLE IF NOT EXISTS flag_status (
                    save_id INTEGER NOT NULL,
                    flag_id TEXT NOT NULL,
                    status BOOLEAN DEFAULT FALSE,
                    PRIMARY KEY (save_id, flag_id),
                    FOREIGN KEY (save_id) REFERENCES saves(save_id),
                    FOREIGN KEY (flag_id) REFERENCES flags(flag_id)
                    );""")

    # === Rooms and Save State Tables ===
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS save_rooms (
            save_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            entered BOOLEAN DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            PRIMARY KEY (save_id, room_id),
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE CASCADE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS save_state (
            save_id INTEGER PRIMARY KEY,
            current_room TEXT,
            previous_room TEXT,
            elapsed_time REAL DEFAULT 0,
            FOREIGN KEY (save_id) REFERENCES saves(save_id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS achievements (
                    achievement_id TEXT PRIMARY KEY,
                    name TEXT UNIQUE,
                    icon TEXT
                   );""")

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS savefile_to_achievement (
                    save_id INTEGER NOT NULL,
                    achievement_id TEXT NOT NULL,
                    PRIMARY KEY (save_id, achievement_id),
                    FOREIGN KEY (save_id) REFERENCES saves(save_id),
                    FOREIGN KEY (achievement_id) REFERENCES achievements(achievement_id)
                   );""")

    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS scoreboard (
                     player_name TEXT PRIMARY KEY,
                     percentage INTEGER,
                     time INTEGER
                 );""")

    # CyberRoom tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cyber_room_state (
            save_id        INTEGER PRIMARY KEY,
            code_unlocked  INTEGER DEFAULT 0,
            completed      INTEGER DEFAULT 0,
            FOREIGN KEY (save_id) REFERENCES saves(save_id)
        );
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS cyber_room_panels (
            save_id   INTEGER NOT NULL,
            panel_id  TEXT    NOT NULL,
            solved    INTEGER DEFAULT 0,
            PRIMARY KEY (save_id, panel_id),
            FOREIGN KEY (save_id) REFERENCES saves(save_id)
        );
    """)

    #dragon room create tables
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
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id),
                     CONSTRAINT fk_object FOREIGN KEY (object_id) REFERENCES dragon_room_objects(object_id)
                 );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_current_npcs (
                     save_id INTEGER,
                     npc_id INTEGER,
                     current_chapter TEXT DEFAULT 'first_chapter',
                     current_node TEXT DEFAULT 'start',
                     PRIMARY KEY (save_id, npc_id),
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id),
                     CONSTRAINT fk_npc FOREIGN KEY (npc_id) REFERENCES dragon_room_npcs(npc_id)
                 );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_current_items (
                     save_id INTEGER,
                     item_id INTEGER,
                     PRIMARY KEY (save_id, item_id),
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id),
                     CONSTRAINT fk_item FOREIGN KEY (item_id) REFERENCES items(item_id)
                   );""")
    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS dragon_room_current_trades (
                     save_id INTEGER,
                     trade_id INTEGER,
                     PRIMARY KEY (save_id, trade_id),
                     CONSTRAINT fk_save FOREIGN KEY (save_id) REFERENCES saves(save_id),
                     CONSTRAINT fk_trade FOREIGN KEY (trade_id) REFERENCES dragon_room_trades(trade_id)
                       );""")
    conn.commit()
    # Insert into common tables
    all_rooms = [
        "cloud_room", "computer_lab", "control_room", "cyber_room", "dragon_room",
        "riddle_room", "roof_garden", "library", "study_landscape",
        "e_w_corridor", "lab_corridor", "n_s_corridor"
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO rooms (name, description) VALUES (?, ?);",
        [(room, "") for room in all_rooms]
    )

    insert_query = "INSERT OR IGNORE INTO items (name) VALUES (?);"
    rows_to_insert = [
        #dragon room
        ('lockpick',),
        ('broadsword',),
        ('sneaking_boots',),
        ('chalk',),
        ('paper',),
        ('invisibility_cloak',),
        ('milk_carton',),
        ('gemstone',),
        ('pickaxe',),
        ('cursed_trophy',),
        #cyberroom
        ('?_key',),
        #riddleroom
        ('magnet',),
        #computerlab
        ('lab_key',),
        #study landscape
        ('rusty_key',),
        ('lab_permit',),
        # library
        ('python_tutorial',),
        # roof garden
        ('cursed_rose',),
        # tbd
        ('beer',),
        ('bootle_opener',),
    ]
    cursor.executemany(insert_query, rows_to_insert)

    insert_query = "INSERT OR IGNORE INTO flags (flag_id) VALUES (?);"
    rows_to_insert = [
        # dragon room
        ('n_s_unlocked',),
        ('finished_tutorial',),
        ('skip_tutorial',),
    ]
    cursor.executemany(insert_query, rows_to_insert)

    insert_query = "INSERT OR IGNORE INTO achievements (achievement_id, name, icon) VALUES (?, ?, ?);"
    rows_to_insert = [
        # general
        ('finish_a_game', 'Finish a game', '🏅',),
        # dragon room
        ('kill_dragon', 'Kill the dragon', '🗡️🐉',),
        ('bribe_dragon', 'Bribe the dragon', '💎',),
        ('steal_trophy', 'Steal the trophy', '🥷🏆',),
        ('destroy_chest', 'Hopefully nothing important was in there...', '💥📦',),
        # roof garden
        ('pet_cat', 'Pet a black cat','🐈‍⬛',),
        #study landscape
        ('coffee_adict', 'Being addicted to coffee', '☕️',),
        ('schoolnerd', 'go back to school', '📓',),
        ('einstein', 'too may attempts', '🤓')
    ]
    cursor.executemany(insert_query, rows_to_insert)

    #dragon room insert data in tables
    with open("rooms/dragon_room_dialog.json", "r", encoding="utf-8") as file:
        dialog_tree = json.load(file)

    insert_query = "INSERT OR IGNORE INTO dragon_room_objects (name, dialog_tree) VALUES (?, ?);"
    rows_to_insert = [
        ('cracked_wall', json.dumps(dialog_tree['dialogue_tree_cracked_wall'])),
        ('blackboard', json.dumps(dialog_tree['dialogue_tree_blackboard'])),
        ('desk', json.dumps(dialog_tree['dialogue_tree_desk'])),
        ('chest', json.dumps(dialog_tree['dialogue_tree_chest'])),
        ('hole', json.dumps(dialog_tree['dialogue_tree_hole'])),
    ]
    cursor.executemany(insert_query, rows_to_insert)

    insert_query = "INSERT OR IGNORE INTO dragon_room_npcs (name, dialog_tree) VALUES (?, ?);"
    rows_to_insert = [
        ('fairy', json.dumps(dialog_tree['dialogue_tree_fairy'])),
        ('kobold', json.dumps(dialog_tree['dialogue_tree_kobold'])),
        ('dragon', json.dumps(dialog_tree['dialogue_tree_dragon'])),
        ('shopkeeper', '')
    ]
    cursor.executemany(insert_query, rows_to_insert)

    cursor.execute("""
        INSERT OR IGNORE INTO dragon_room_trades (sale_item, wanted_item)
        SELECT sale.item_id, wanted.item_id
        FROM (SELECT name, item_id FROM items) AS sale
        JOIN (SELECT name, item_id FROM items) AS wanted
        WHERE sale.name = 'gemstone' AND wanted.name = 'broadsword'
            OR sale.name = 'chalk' AND wanted.name = 'sneaking_boots'
            OR sale.name = 'pickaxe' AND wanted.name = 'lockpick';
                    """)
    conn.commit()

    return

def create_new_save(state, current_player_name):
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO players (player_name) VALUES (?)", (current_player_name,))

    cursor.execute("SELECT player_id FROM players WHERE player_name = ?", (current_player_name,))
    player_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO saves (player_id) VALUES (?)", (player_id,))
    save_id = cursor.lastrowid
    state["save_id"] = save_id

    # --- Initialize new save state ---
    cursor.execute("""
        INSERT INTO save_state (save_id, current_room, previous_room, elapsed_time)
        VALUES (?, ?, ?, 0);
    """, (save_id, "study_landscape", "study_landscape"))

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

    #dragon room
    current_object_names = ('cracked_wall', 'blackboard', 'desk', 'chest', 'hole',)
    placeholders = ','.join(['?'] * len(current_object_names))
    insert_query = f"""
            INSERT INTO dragon_room_current_objects (save_id, object_id)
            SELECT ?, object_id
            FROM dragon_room_objects
            WHERE name IN ({placeholders});
    """
    cursor.execute(insert_query, (save_id, *current_object_names))

    current_item_names = ('pickaxe',)
    placeholders = ','.join(['?'] * len(current_item_names))
    insert_query = f"""
            INSERT INTO dragon_room_current_items (save_id, item_id)
            SELECT ?, item_id
            FROM items
            WHERE name IN ({placeholders});
        """
    cursor.execute(insert_query, (save_id, *current_item_names))

    cursor.execute("""
            INSERT INTO dragon_room_current_trades (save_id, trade_id)
            SELECT ?, trade_id
            FROM dragon_room_trades;
            """, (save_id,))

    conn.commit()
    return

def list_saves(conn):
    return conn.execute("""
            SELECT s.save_id, p.player_name, ss.current_room, s.saved_at
            FROM saves s
            JOIN players p ON s.player_id = p.player_id
            LEFT JOIN save_state ss ON s.save_id = ss.save_id
            ORDER BY s.saved_at DESC;
        """).fetchall()

def delete_save(state, save_id):
    conn = state["db_conn"]
    cursor = conn.cursor()
    cursor.execute("""
        SELECT CASE
        WHEN EXISTS (SELECT 1
        FROM saves
        WHERE save_id = ?)
        THEN 1
        ELSE 0
        END;""", (save_id,))
    row = cursor.fetchone()

    if row[0]:
        cursor.execute("DELETE FROM dragon_room_current_npcs WHERE save_id = ?;", (save_id,))
        cursor.execute("DELETE FROM dragon_room_current_items WHERE save_id = ?;", (save_id,))
        cursor.execute("DELETE FROM dragon_room_current_objects WHERE save_id = ?;", (save_id,))
        cursor.execute("DELETE FROM dragon_room_current_trades WHERE save_id = ?;", (save_id,))
        cursor.execute("DELETE FROM inventory WHERE save_id = ?;", (save_id,))
        cursor.execute("DELETE FROM saves WHERE save_id = ?;", (save_id,))
        conn.commit()
        print("Save deleted.")
    else:
        print("Save not found.")