# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================
import time


# Functions to easily interact with the database

def db_is_item_in_inventory(state, item_name):
    save_id = state["save_id"]
    conn = state["db_conn"]

    cursor = conn.cursor()
    cursor.execute("""
    SELECT CASE 
    WHEN EXISTS (
        SELECT 1 
        FROM inventory i
        JOIN items it ON i.item_id = it.item_id
        WHERE i.save_id = ? AND it.name = ?
    ) THEN 1 ELSE 0 
    END;
    """, (save_id, item_name,))
    row = cursor.fetchone()
    return row[0]

def db_add_item_to_inventory(state, item_name):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO inventory (save_id, item_id)
    SELECT ?, item_id
    FROM items
    WHERE name = ?
    """, (current_save_id, item_name,))
    conn.commit()
    return

def db_remove_item_from_inventory(state, item_name):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM inventory
    WHERE save_id = ?
    AND item_id IN (
    SELECT item_id FROM items WHERE name = ?);
                   """, (current_save_id, item_name,))
    conn.commit()
    return

def db_get_all_items_in_inventory(state):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    SELECT it.name
        FROM inventory i
        JOIN items it ON i.item_id = it.item_id
        WHERE i.save_id = ?;
                   """, (current_save_id,))
    rows = cursor.fetchall()
    item_list = [item[0] for item in rows]
    return item_list

def db_get_player_name(state):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.player_name
        FROM saves s
        JOIN players p ON p.player_id = s.player_id
        WHERE s.save_id = ?;
                   """, (current_save_id,))
    rows = cursor.fetchone()
    return rows[0]

def db_set_flag(state, flag_name, flag):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
                UPDATE flag_status
                    SET ? = ?
                    WHERE save_id = ?
                   """, (flag_name, flag, current_save_id,))
    conn.commit()

def db_get_flag(state, flag_name):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
                SELECT ? 
                    FROM flag_status
                    WHERE save_id = ?
                    """, (flag_name, current_save_id,))
    rows = cursor.fetchone()
    return rows

def db_mark_room_entered(state, room_name):
    #Mark room as entered for current save

    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("SELECT room_id FROM rooms WHERE name = ?;", (room_name,))
    row = cursor.fetchone()
    if not row:
        print(f"Room '{room_name}' not found in rooms table.")
        return
    room_id = row[0]

    cursor.execute("""
        UPDATE save_rooms
        SET entered = 1
        WHERE save_id = ? AND room_id = ?;
    """, (save_id, room_id))
    conn.commit()

def db_mark_room_completed(state, room_name):
    #Mark a room as completed for given save
    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("SELECT room_id FROM rooms WHERE name = ?;", (room_name,))
    row = cursor.fetchone()
    if not row:
        print(f"Room '{room_name}' not found in rooms table.")
        return
    room_id = row[0]

    cursor.execute("""
        UPDATE save_rooms
        SET completed = 1
        WHERE save_id = ? AND room_id = ?;
    """, (save_id, room_id))
    conn.commit()

def db_get_completed_status_of_all_rooms(state):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    SELECT entered
        FROM save_rooms
        WHERE save_id = ?;
                   """, (current_save_id,))
    rows = cursor.fetchall()
    item_list = [item[0] for item in rows]
    return item_list

def db_award_achievement(state, achievement_name):
    print("You got an achievement!")
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO savefile_to_achievement (save_id, achievement_id)
    VALUES (?, ?)
    """, (current_save_id, achievement_name,))
    conn.commit()
    return

def db_get_all_achievements_of_a_save(state, save_id):
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    SELECT a.icon
        FROM savefile_to_achievement sa
        JOIN achievements a ON sa.achievement_id = a.achievement_id
        WHERE sa.save_id = ?
        ORDER BY a.achievement_id ASC;
                   """, (save_id,))
    rows = cursor.fetchall()
    achievement_list = [item[0] for item in rows]
    return achievement_list

def db_get_all_achievements_of_a_player(state, player_name):
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    SELECT DISTINCT a.icon
        FROM savefile_to_achievement sa
        JOIN achievements a ON sa.achievement_id = a.achievement_id
        JOIN saves s ON s.save_id = sa.save_id
        JOIN players p ON p.player_id = s.player_id
        WHERE p.player_name = ?
        ORDER BY a.achievement_id ASC;
                   """, (player_name,))
    rows = cursor.fetchall()
    achievement_list = [item[0] for item in rows]
    return achievement_list

def db_get_room_completed(state, room_name):
    #Return status of completion for given room name, TRUE/FALSE

    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sr.completed
        FROM save_rooms sr
        JOIN rooms r ON sr.room_id = r.room_id
        WHERE sr.save_id = ? AND r.name = ?;
    """, (save_id, room_name))
    row = cursor.fetchone()
    return bool(row and row[0])

def db_get_room_entered(state, room_name):
    #Return status of completion for given room name, TRUE/FALSE

    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sr.entered
        FROM save_rooms sr
        JOIN rooms r ON sr.room_id = r.room_id
        WHERE sr.save_id = ? AND r.name = ?;
    """, (save_id, room_name))
    row = cursor.fetchone()
    return bool(row and row[0])


def db_set_current_room(state, new_room_name):
    #Update the current room and the previous room

    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("SELECT current_room FROM save_state WHERE save_id = ?;", (save_id,))
    row = cursor.fetchone()
    previous_room = row[0] if row and row[0] else None

    cursor.execute("""
        UPDATE save_state
        SET previous_room = ?, current_room = ?
        WHERE save_id = ?;
    """, (previous_room, new_room_name, save_id))
    conn.commit()

def db_get_current_room(state):
    #Return the current room name

    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("SELECT current_room FROM save_state WHERE save_id = ?;", (save_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def db_get_previous_room(state):
    #Return the current room name

    conn = state["db_conn"]
    save_id = state["save_id"]
    cursor = conn.cursor()

    cursor.execute("SELECT previous_room FROM save_state WHERE save_id = ?;", (save_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def db_update_elapsed_time(state):
    conn = state["db_conn"]
    save_id = state["save_id"]
    elapsed = time.time() - state["start_time"]

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE save_state
        SET elapsed_time = ?
        WHERE save_id = ?;
    """, (elapsed, save_id))
    conn.commit()

def db_get_elapsed_time(state):
    conn = state["db_conn"]
    save_id = state["save_id"]

    cursor = conn.cursor()
    cursor.execute("""
        SELECT elapsed_time
        FROM save_state
        WHERE save_id = ?;
    """, (save_id,))
    row = cursor.fetchone()
    return row[0] if row else None

