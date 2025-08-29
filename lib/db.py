import sqlite3

def get_db():
    """
    Returns a new connection and cursor to the SQLite database.
    Usage:
        conn, cursor = get_db()
    """
    conn = sqlite3.connect("vaccine_reminder.db")
    cursor = conn.cursor()
    return conn, cursor
