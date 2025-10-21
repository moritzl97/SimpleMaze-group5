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

    cursor.execute("""
                 CREATE TABLE IF NOT EXISTS scoreboard (
                     player_name TEXT PRIMARY KEY,
                     percentage INTEGER,
                     time INTEGER
                 );""")

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
        ('trophy',),
        #cyberroom
        ('cyber_key',),
        #riddleroom
        ('magnet',),
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

def save_state(player_name: str, state: dict):
    conn = state["db_conn"]
    payload = json.dumps(state, ensure_ascii=False, separators=(",", ":"))
    current_room = state.get("current_room") or "start"
    now = now_iso()
    conn.execute("""
      INSERT INTO saves (player_name, state_json, current_room, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?)
      ON CONFLICT(player_name) DO UPDATE SET
        state_json   = excluded.state_json,
        current_room = excluded.current_room,
        updated_at   = excluded.updated_at;
    """, (player_name, payload, current_room, now, now))
    conn.commit()

def load_state(conn, player_name: str):
    row = conn.execute("SELECT state_json FROM saves WHERE player_name = ?;", (player_name,)).fetchone()
    return json.loads(row[0]) if row else None

def list_saves(conn):
    return conn.execute("""
      SELECT player_name, current_room, updated_at
      FROM saves
      ORDER BY updated_at DESC;
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