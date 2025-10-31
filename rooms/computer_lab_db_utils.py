# db utils for computer lab
import time

def cl_get_state(state):
    conn = state["db_conn"]
    save_id = state["save_id"]
    cur = conn.cursor()

    cur.execute("""
        SELECT riddle_answer, laptop_unlocked, laptop_softlocked
        FROM computer_lab_state
        WHERE save_id = ?;
    """, (save_id,))
    row = cur.fetchone()

    if not row:
        cur.execute("""
            INSERT INTO computer_lab_state (save_id, riddle_answer, laptop_unlocked, laptop_softlocked)
            VALUES (?, 0, 0, 0);
        """, (save_id,))
        for seminar in ("python programming", "database & data structures", "intercultural collaboration", "professional skills"):
            cur.execute("""
                INSERT INTO computer_lab_seminars (save_id, seminar_name)
                VALUES (?, ?)
                ON CONFLICT(save_id, seminar_name) DO NOTHING;
            """, (save_id, seminar))
        conn.commit()
        return {
            "riddle_answer": False,
            "laptop_unlocked": False,
            "laptop_softlocked": 0,
            "seminars": {s: False for s in ("python programming", "database & data structures", "intercultural collaboration", "professional skills")}
        }

    cur.execute("""
        SELECT seminar_name, completed
        FROM computer_lab_seminars
        WHERE save_id = ?;
    """, (save_id,))
    seminar_rows = cur.fetchall()
    seminars = {name: bool(done) for name, done in seminar_rows}

    return {
        "riddle_answer": bool(row[0]),
        "laptop_unlocked": bool(row[1]),
        "laptop_softlocked": row[2],
        "seminars": seminars
    }

def cl_set_riddle_answer(state, solved: bool):
    conn = state["db_conn"]
    save_id = state["save_id"]
    conn.execute("""
        UPDATE computer_lab_state
           SET riddle_answer = ?
         WHERE save_id = ?;
    """, (1 if solved else 0, save_id))
    conn.commit()

def cl_check_riddle_answer(state):
    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.execute("""
        SELECT riddle_answer
          FROM computer_lab_state
         WHERE save_id = ?;
    """, (save_id,))
    result = cursor.fetchone()
    return bool(result and result[0] == 1)


def cl_set_laptop_unlocked(state, unlocked: bool):
    conn = state["db_conn"]
    save_id = state["save_id"]
    conn.execute("""
        UPDATE computer_lab_state
           SET laptop_unlocked = ?
         WHERE save_id = ?;
    """, (1 if unlocked else 0, save_id))
    conn.commit()

def cl_is_laptop_unlocked(state):
    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.execute("""
        SELECT laptop_unlocked
          FROM computer_lab_state
         WHERE save_id = ?;
    """, (save_id,))
    result = cursor.fetchone()
    return bool(result and result[0] == 1)


def cl_set_softlock_value(state, value: float):
    conn = state["db_conn"]
    save_id = state["save_id"]
    unlock_time = time.time() + value
    conn.execute("""
        UPDATE computer_lab_state
           SET laptop_softlocked = ?
         WHERE save_id = ?;
    """, (unlock_time, save_id))
    conn.commit()
    return unlock_time

def cl_check_softlock_value(state):
    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.execute("""
        SELECT laptop_softlocked
          FROM computer_lab_state
         WHERE save_id = ?;
    """, (save_id,))
    result = cursor.fetchone()
    return result[0] if result and result[0] is not None else None

def cl_mark_seminar_completed(state, seminar_name: str):
    # marks a specific seminar as completed
    conn = state["db_conn"]
    save_id = state["save_id"]
    conn.execute("""
        UPDATE computer_lab_seminars
           SET completed = 1
         WHERE save_id = ? AND seminar_name = ?;
    """, (save_id, seminar_name))
    conn.commit()


def cl_is_seminar_completed(state, seminar_name: str) -> bool:
    # checks if the seminar is completed
    conn = state["db_conn"]
    save_id = state["save_id"]
    cur = conn.cursor()
    cur.execute("""
        SELECT completed FROM computer_lab_seminars
         WHERE save_id = ? AND seminar_name = ?;
    """, (save_id, seminar_name))
    row = cur.fetchone()
    return bool(row[0]) if row else False


def cl_are_all_seminars_completed(state) -> bool:
    # checks if all the seminars are completed
    conn = state["db_conn"]
    save_id = state["save_id"]
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) = 4
          FROM computer_lab_seminars
         WHERE save_id = ? AND completed = 1;
    """, (save_id,))
    (all_done,) = cur.fetchone()
    return bool(all_done)

