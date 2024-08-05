import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create chat table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat (
                id INTEGER PRIMARY KEY,
                name TEXT,
                max_token INTEGER,
                temperature REAL
            );
        ''')
        # Create message table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                role TEXT,
                content TEXT,
                FOREIGN KEY(chat_id) REFERENCES chat(id)
            )
        ''')
        conn.commit()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
