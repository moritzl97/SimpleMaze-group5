from game.db_utils import *

def cloud_db_get_state(state):
    """Fetch the current Cloud Room state for this save."""
    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("""
        SELECT robot_locked, quiz_passed
        FROM cloud_room_state
        WHERE save_id = ?;
    """, (save_id,))
    row = cursor.fetchone()

    if not row:
        # Initialize if missing
        cursor.execute("""
            INSERT INTO cloud_room_state (save_id, robot_locked, quiz_passed)
            VALUES (?, 1, 0);
        """, (save_id,))
        conn.commit()
        return {"robot_locked": True, "quiz_passed": False}

    return {"robot_locked": bool(row[0]), "quiz_passed": bool(row[1])}


def cloud_db_set_robot_locked(state, locked: bool):
    conn = state["db_conn"]
    save_id = state["save_id"]
    conn.execute("""
        UPDATE cloud_room_state
        SET robot_locked = ?
        WHERE save_id = ?;
    """, (1 if locked else 0, save_id))
    conn.commit()


def cloud_db_set_quiz_passed(state, passed: bool):
    conn = state["db_conn"]
    save_id = state["save_id"]
    conn.execute("""
        UPDATE cloud_room_state
        SET quiz_passed = ?
        WHERE save_id = ?;
    """, (1 if passed else 0, save_id))
    conn.commit()
