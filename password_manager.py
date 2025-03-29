import sqlite3
import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox
import pyperclip

def load_passwords(user_id, search_query=""):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT id, website, username, password FROM passwords WHERE user_id=? AND website LIKE ?", (user_id, f"%{search_query}%"))
    else:
        cursor.execute("SELECT id, website, username, password FROM passwords WHERE user_id=?", (user_id,))
    passwords = cursor.fetchall()
    conn.close()
    return passwords

def save_password(user_id, website, username, password):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (user_id, website, username, password) VALUES (?, ?, ?, ?)",
                   (user_id, website, username, password))
    conn.commit()
    conn.close()
def add_password(self):
    add_window = Toplevel()
    add_window.title("Add New Password")

    tk.Label(add_window, text="Website:").pack()
    website_entry = tk.Entry(add_window)
    website_entry.pack()

    tk.Label(add_window, text="Username:").pack()
    username_entry = tk.Entry(add_window)
    username_entry.pack()

    tk.Label(add_window, text="Password:").pack()
    password_entry = tk.Entry(add_window, show="*")
    password_entry.pack()

    def save_new_password():
        save_password(self.current_user, website_entry.get(), username_entry.get(), password_entry.get())
        messagebox.showinfo("Success", "Password saved successfully.")
        add_window.destroy()
        self.load_passwords()

    tk.Button(add_window, text="Save", command=save_new_password).pack()
    tk.Button(add_window, text="Cancel", command=add_window.destroy).pack()


def copy_password(password):
    pyperclip.copy(password)
    messagebox.showinfo("Success", "Password copied to clipboard!")

def edit_password(password_id):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT website, username, password FROM passwords WHERE id=?", (password_id,))
    password_data = cursor.fetchone()
    conn.close()

    if not password_data:
        messagebox.showerror("Error", "Password not found.")
        return

    edit_window = Toplevel()
    edit_window.title("Edit Password")

    Label(edit_window, text="Website:").pack()
    website_entry = Entry(edit_window)
    website_entry.insert(0, password_data[0])
    website_entry.pack()

    Label(edit_window, text="Username:").pack()
    username_entry = Entry(edit_window)
    username_entry.insert(0, password_data[1])
    username_entry.pack()

    Label(edit_window, text="Password:").pack()
    password_entry = Entry(edit_window, show="*")
    password_entry.insert(0, password_data[2])
    password_entry.pack()

    def save_changes():
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE passwords SET website=?, username=?, password=? WHERE id=?",
                       (website_entry.get(), username_entry.get(), password_entry.get(), password_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password updated successfully.")
        edit_window.destroy()

    Button(edit_window, text="Save", command=save_changes).pack()
    Button(edit_window, text="Cancel", command=edit_window.destroy).pack()
