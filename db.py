import sqlite3
import random
import string
from contextlib import closing

path = "urls.db"
chars = string.ascii_letters + string.digits

def _connect():
    return sqlite3.connect(path)

def init_db():
    with closing(_connect()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                long_url  TEXT NOT NULL UNIQUE,
                short_url TEXT NOT NULL UNIQUE
            )
            """
        )

def generate(length = 6):
    return "".join(random.choice(chars) for i in range(length))

def get_all_urls():
    with closing(_connect()) as conn:
        rows = conn.execute("SELECT short_url FROM urls").fetchall()
        return [row[0] for row in rows]

def link_to_long(long_url, short_url):
    with closing(_connect()) as conn:
        conn.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, short_url))
        conn.commit()  

def check_short(long_url):
    with closing(_connect()) as conn:
        row = conn.execute("SELECT short_url FROM urls WHERE long_url = ?", (long_url,)).fetchone()
    return row[0] if row else None

def check_long(short_url):
    """Return the long URL for a short code, or None."""
    with closing(_connect()) as conn:
        row = conn.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,)).fetchone()
    return row[0] if row else None