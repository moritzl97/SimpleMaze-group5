def db_get_book_list(state):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lb.title
            FROM library_state ls
            JOIN library_books lb ON lb.book_id = ls.book_id
            WHERE ls.save_id = ?
            ORDER BY lb.book_id ASC;
       """, (current_save_id,))
    rows = cursor.fetchall()
    book_list = [item[0] for item in rows]
    return book_list

def db_remove_next_book(state, book_name):
    current_save_id = state["save_id"]
    conn = state["db_conn"]
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM library_state
    WHERE save_id = ?
    AND book_id IN (
    SELECT book_id FROM library_books WHERE title = ?);
                   """, (current_save_id, book_name,))
    conn.commit()