# =============================================================================
# Project: Escape of the Nightmare
# Authors: Moritz Lackner, Oskar Lukáč, Dominika Nowakiewicz,
#          Mihail Petrov, Rodrigo Polo Lopez, Tieme van Rees
# Course:  Application Development, Applied Computer Science 2025/26
# School:  The Hague University of Applied Sciences (THUAS)
# =============================================================================

import json

def db_check_if_in_room(state, data, object_type):
    save_id = state["save_id"]
    conn = state["db_conn"]

    cursor = conn.cursor()
    if object_type == "objects":
        cursor.execute("""
                       SELECT CASE
                       WHEN EXISTS (SELECT 1
                            FROM dragon_room_current_objects co
                            JOIN dragon_room_objects o ON o.object_id = co.object_id
                            WHERE co.save_id = ?
                            AND o.name = ?) THEN 1
                            ELSE 0
                            END;
                       """, (save_id, data,))
    elif object_type == "npcs":
        cursor.execute("""
                       SELECT CASE
                            WHEN EXISTS (SELECT 1
                            FROM dragon_room_current_npcs cn
                            JOIN dragon_room_npcs n ON n.npc_id = cn.npc_id
                            WHERE cn.save_id = ?
                            AND n.name = ?) THEN 1
                            ELSE 0
                            END;
                       """, (save_id, data,))
    elif object_type == "items":
        cursor.execute("""
                       SELECT CASE
                            WHEN EXISTS (SELECT 1
                            FROM dragon_room_current_items ci
                            JOIN items i ON i.item_id = ci.item_id
                            WHERE ci.save_id = ?
                            AND i.name = ?) THEN 1
                            ELSE 0
                            END;
                       """, (save_id, data,))
    row = cursor.fetchone()
    return row[0]

def db_get_objects_in_room(state, object_type):
    save_id = state["save_id"]
    conn = state["db_conn"]

    cursor = conn.cursor()
    if object_type == "objects":
        cursor.execute("""
                       SELECT o.name
                            FROM dragon_room_current_objects co
                            JOIN dragon_room_objects o ON o.object_id = co.object_id
                            WHERE co.save_id = ?;
                       """, (save_id,))
    elif object_type == "npcs":
        cursor.execute("""
                       SELECT n.name
                            FROM dragon_room_current_npcs cn
                            JOIN dragon_room_npcs n ON n.npc_id = cn.npc_id
                            WHERE cn.save_id = ?;
                       """, (save_id,))
    elif object_type == "items":
        cursor.execute("""
                       SELECT i.name
                            FROM dragon_room_current_items ci
                            JOIN items i ON i.item_id = ci.item_id
                            WHERE ci.save_id = ?;
                       """, (save_id,))
    rows = cursor.fetchall()
    row_list = [row[0] for row in rows]
    return row_list

def db_remove_object_from_room(state, data, object_type):
    save_id = state["save_id"]
    conn = state["db_conn"]

    cursor = conn.cursor()
    if object_type == "objects":
        cursor.execute("""
                        DELETE FROM dragon_room_current_objects
                            WHERE save_id = ?
                            AND object_id IN (SELECT object_id FROM dragon_room_objects WHERE name = ?);
               """, (save_id, data,))
    elif object_type == "npcs":
        cursor.execute("""
                        DELETE FROM dragon_room_current_npcs
                            WHERE save_id = ?
                            AND npc_id IN (SELECT npc_id FROM dragon_room_npcs WHERE name = ?);
               """, (save_id, data,))
    elif object_type == "items":
        cursor.execute("""
                        DELETE FROM dragon_room_current_items
                            WHERE save_id = ?
                            AND item_id IN (SELECT item_id FROM items WHERE name = ?);
                       """, (save_id, data,))
    conn.commit()
    return

def db_add_object_to_room(state, data, object_type):
    save_id = state["save_id"]
    conn = state["db_conn"]

    cursor = conn.cursor()
    if object_type == "objects":
        cursor.execute("""
                       INSERT INTO dragon_room_current_objects (save_id, object_id)
                       SELECT ?, object_id
                       FROM dragon_room_objects
                       WHERE name = ?
                       """, (save_id, data,))
    elif object_type == "npcs":
        cursor.execute("""
                       INSERT INTO dragon_room_current_npcs (save_id, npc_id)
                       SELECT ?, npc_id
                       FROM dragon_room_npcs
                       WHERE name = ?
                       """, (save_id, data,))
    elif object_type == "items":
        cursor.execute("""
                       INSERT INTO dragon_room_current_items (save_id, item_id)
                       SELECT ?, item_id
                       FROM items
                       WHERE name = ?
                       """, (save_id, data,))
    conn.commit()
    return

def db_get_dialog(state, name):
    conn = state["db_conn"]
    cursor = conn.cursor()
    cursor.execute("""
                        SELECT dialog_tree FROM dragon_room_npcs WHERE name = ?
                        UNION
                        SELECT dialog_tree FROM dragon_room_objects WHERE name = ?;
                       """, (name,name,))
    row = cursor.fetchone()
    json_string = row[0]
    dialog_dict = json.loads(json_string)
    return dialog_dict

def db_get_chapter_node_index(state, name):
    save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()
    cursor.execute("""
                        SELECT current_chapter, current_node FROM dragon_room_current_npcs WHERE save_id = ? AND npc_id IN (SELECT npc_id FROM dragon_room_npcs WHERE name = ?)
                        UNION
                        SELECT current_chapter, current_node FROM dragon_room_current_objects WHERE save_id = ? AND object_id IN (SELECT object_id FROM dragon_room_objects WHERE name = ?);
                       """, (save_id, name, save_id, name,))
    row = cursor.fetchone()
    return row

def db_save_chapter_node(state, name, node, chapter = None):
    save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()
    if chapter is not None:
        cursor.execute("""
                        UPDATE dragon_room_current_npcs
                            SET current_chapter = ?,
                            current_node = ?
                            WHERE save_id = ? AND npc_id IN (SELECT npc_id FROM dragon_room_npcs WHERE name = ?)
                           """, (chapter, node, save_id, name))
        cursor.execute("""
                       UPDATE dragon_room_current_objects
                       SET current_chapter = ?,
                           current_node    = ?
                       WHERE save_id = ? AND object_id IN (SELECT object_id FROM dragon_room_objects WHERE name = ?)
                       """, (chapter, node, save_id, name))
    else:
        cursor.execute("""
                       UPDATE dragon_room_current_npcs
                       SET current_node = ?
                       WHERE save_id = ? AND npc_id IN (SELECT npc_id FROM dragon_room_npcs WHERE name = ?)
                       """, (node, save_id, name))
        cursor.execute("""
                       UPDATE dragon_room_current_objects
                       SET current_node = ?
                       WHERE save_id = ? AND object_id IN (SELECT object_id FROM dragon_room_objects WHERE name = ?)
                       """, (node, save_id, name))
    conn.commit()
    return

def db_get_trades(state):
    save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT t.trade_id, wanted_item.name, sale_item.name
                        FROM dragon_room_current_trades AS ct
                        JOIN dragon_room_trades AS t ON ct.trade_id = t.trade_id
                        JOIN items AS wanted_item ON t.wanted_item = wanted_item.item_id
                        JOIN items AS sale_item ON t.sale_item = sale_item.item_id
                        WHERE ct.save_id = ?;
                   """, (save_id,))
    rows = cursor.fetchall()
    #row_list = [row[0] for row in rows]
    return rows

def db_remove_trade(state, trade_id):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
                   DELETE
                   FROM dragon_room_current_trades
                   WHERE save_id = ? AND trade_id = ?;
                   """, (current_save_id, trade_id,))
    conn.commit()
