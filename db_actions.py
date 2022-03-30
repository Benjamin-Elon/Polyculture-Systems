import sqlite3


def dict_factory(cursor, row):
    """Causes sqlite to return dictionary instead of tuple"""
    """Easier and more pythonic than using indices"""

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_to_db():
    conn = sqlite3.connect(r"Syntropy.sqlite")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    print("Done.")
    return conn, cur


def close_database(cur):
    """Closes the database"""
    cur.close()
    return
