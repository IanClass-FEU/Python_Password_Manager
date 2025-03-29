import sqlite3

def init_db():
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        birthday TEXT,
        gender TEXT,
        username TEXT UNIQUE, 
        password TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY, 
        user_id INTEGER,
        website TEXT, 
        username TEXT, 
        password TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect("passwords.db")
