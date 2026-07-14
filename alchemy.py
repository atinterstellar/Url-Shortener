import sqlite3

conn = sqlite3.connect('urls.db')
cur = conn.cursor()

create_table1 = '''CREATE TABLE IF NOT EXISTS
URLS(long TEXT PRIMARY KEY, short TEXT)'''
cur.execute(create_table1)

def add_row(long,short):
    command = f'''INSERT INTO urls VALUES(?,?)'''
    cur.execute(command, (long, short))
    conn.commit()

def delete(long):
    command = f'DELETE FROM urls WHERE long = ?'
    cur.execute(command, (long,))
    conn.commit()

def fetch(short):
    command = '''SELECT long FROM urls WHERE short = ?'''
    cur.execute(command , (short,))
    long = cur.fetchone()
    return long[0] if long else None

