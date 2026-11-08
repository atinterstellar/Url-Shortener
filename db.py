import sqlite3
import random
import string

conn = sqlite3.connect('urls.db')

c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS urls (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                long_url  TEXT NOT NULL UNIQUE,
                short_url TEXT NOT NULL UNIQUE
            )
''')

def generate(length = 6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for i in range(length))
    return short_url

def get_all_urls():
    c.execute('SELECT short_url FROM urls')
    short_urls = [row[0] for row in c.fetchall()]
    return short_urls

def link_to_long(long_url, short_url):
    c.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, short_url))
    conn.commit()  

def check_short(long_url):
    c.execute("SELECT short_url FROM urls WHERE long_url = ?", (long_url,))
    row = c.fetchone()
    return row[0] if row else None

def check_long(short_url):
    c.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,))
    row = c.fetchone()
    return row[0] if row else None