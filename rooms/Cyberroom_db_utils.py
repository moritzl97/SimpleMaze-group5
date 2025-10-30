
# CyberRoom DB utilities (simplified)
# Saves and loads: panel progress and terminal unlocked flag.

def _ensure_state_row(state):
    save_id = state["save_id"]
    conn = state["db_conn"]
    cur = conn.cursor()

    # ensure state row
    cur.execute("""
        INSERT INTO cyber_room_state (save_id)
        VALUES (?)
        ON CONFLICT(save_id) DO NOTHING;
    """, (save_id,))

    # ensure 3 panel rows
    for pid in ("1", "2", "3"):
        cur.execute("""
            INSERT INTO cyber_room_panels (save_id, panel_id)
            VALUES (?, ?)
            ON CONFLICT(save_id, panel_id) DO NOTHING;
        """, (save_id, pid))

    conn.commit()


# Panel flags

def cr_mark_panel_solved(state, panel_id: str):
    _ensure_state_row(state)
    save_id = state["save_id"]
    conn = state["db_conn"]
    cur = conn.cursor()

    cur.execute("""
        UPDATE cyber_room_panels
           SET solved = 1
         WHERE save_id = ? AND panel_id = ?;
    """, (save_id, panel_id))
    conn.commit()


def cr_is_panel_solved(state, panel_id: str) -> bool:
    _ensure_state_row(state)
    save_id = state["save_id"]
    conn = state["db_conn"]
    cur = conn.cursor()

    cur.execute("""
        SELECT solved FROM cyber_room_panels
         WHERE save_id = ? AND panel_id = ?;
    """, (save_id, panel_id))
    row = cur.fetchone()
    return bool(row[0]) if row else False


def cr_are_all_panels_solved(state) -> bool:
    _ensure_state_row(state)
    save_id = state["save_id"]
    conn = state["db_conn"]
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) = 3
          FROM cyber_room_panels
         WHERE save_id = ? AND solved = 1;
    """, (save_id,))
    (all_solved,) = cur.fetchone()
    return bool(all_solved)


# Terminal flag

def cr_set_terminal_unlocked(state, value: bool):
    _ensure_state_row(state)
    save_id = state["save_id"]
    conn = state["db_conn"]
    cur = conn.cursor()

    cur.execute("""
        UPDATE cyber_room_state
           SET code_unlocked = ?
         WHERE save_id = ?;
    """, (1 if value else 0, save_id))
    conn.commit()


def cr_is_terminal_unlocked(state) -> bool:
    _ensure_state_row(state)
    save_id = state["save_id"]
    conn = state["db_conn"]
    cur = conn.cursor()

    cur.execute("""
        SELECT code_unlocked FROM cyber_room_state WHERE save_id = ?;
    """, (save_id,))
    row = cur.fetchone()
    return bool(row[0]) if row else False
