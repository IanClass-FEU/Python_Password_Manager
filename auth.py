import sqlite3
from tkinter import messagebox
from database import get_db_connection

def login(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def register_user(first_name, middle_name, last_name, birthday, gender, username, password):
    if not (first_name and last_name and birthday and gender and username and password):
        messagebox.showerror("Error", "All fields except middle name are required")
        return False
    
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("""
        INSERT INTO users (first_name, middle_name, last_name, birthday, gender, username, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (first_name, middle_name, last_name, birthday, gender, username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Account created successfully!")
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
        return False
