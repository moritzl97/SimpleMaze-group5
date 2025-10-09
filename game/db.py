# db.py
import sqlite3, json, datetime

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"
def now_iso(): return datetime.datetime.now(datetime.UTC).strftime(ISO)

def init_db(path: str = "saves.db"):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("""
      CREATE TABLE IF NOT EXISTS saves (
        player_name   TEXT PRIMARY KEY,
        state_json    TEXT NOT NULL,
        current_room  TEXT NOT NULL,
        created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
        updated_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
      );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_saves_updated_at ON saves(updated_at DESC);")
    conn.commit()
    return conn

def save_state(conn, player_name: str, state: dict):
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
