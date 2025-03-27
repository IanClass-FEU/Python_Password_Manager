import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

# Database setup
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    website TEXT,
    user TEXT,
    password TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
)
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    username = reg_user_entry.get()
    password = reg_pass_entry.get()
    hashed_password = hash_password(password)
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists!")
        return
    
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    messagebox.showinfo("Success", "Account created! You can now log in.")
    reg_frame.pack_forget()
    login_frame.pack()

def login():
    global current_user
    username = user_entry.get()
    password = pass_entry.get()
    hashed_password = hash_password(password)
    
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    if cursor.fetchone():
        current_user = username
        login_frame.pack_forget()
        main_ui()
    else:
        messagebox.showerror("Error", "Invalid credentials!")

def logout():
    global current_user
    current_user = None
    main_frame.pack_forget()
    login_frame.pack()

def main_ui():
    global site_entry, user_entry, password_entry, search_entry, list_frame
    main_frame.pack()
    
    tk.Label(main_frame, text=f"Logged in as: {current_user}").pack()
    tk.Button(main_frame, text="Logout", command=logout).pack()
    
    tk.Label(main_frame, text="Website").pack()
    site_entry = tk.Entry(main_frame)
    site_entry.pack()
    
    tk.Label(main_frame, text="Username").pack()
    user_entry = tk.Entry(main_frame)
    user_entry.pack()
    
    tk.Label(main_frame, text="Password").pack()
    password_entry = tk.Entry(main_frame, show="*")
    password_entry.pack()
    
    tk.Button(main_frame, text="Add Password", command=add_password).pack()
    
    tk.Label(main_frame, text="Search").pack()
    search_entry = tk.Entry(main_frame)
    search_entry.pack()
    search_entry.bind("<KeyRelease>", lambda e: display_passwords(search_entry.get()))
    
    list_frame = tk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True)
    display_passwords()

def display_passwords(search_query=""):
    for widget in list_frame.winfo_children():
        widget.destroy()
    
    cursor.execute("SELECT website, user, password FROM passwords WHERE username = ?", (current_user,))
    passwords = cursor.fetchall()
    
    for site, user, pwd in passwords:
        if search_query.lower() in site.lower():
            frame = tk.Frame(list_frame, bd=2, relief=tk.SUNKEN)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(frame, text=f"Website: {site}").pack(anchor='w')
            tk.Label(frame, text=f"Username: {user}").pack(anchor='w')
            password_label = tk.Label(frame, text="Password: *****")
            password_label.pack(anchor='w')
            
            def toggle_password(lbl=password_label, pwd=pwd):
                lbl.config(text=f"Password: {pwd}" if lbl.cget("text") == "Password: *****" else "Password: *****")
            
            tk.Button(frame, text="Show", command=toggle_password).pack(side=tk.LEFT)
            
            if PYPERCLIP_AVAILABLE:
                def copy_password(pwd=pwd):
                    pyperclip.copy(pwd)
                    messagebox.showinfo("Copied", "Password copied to clipboard!")
                tk.Button(frame, text="Copy", command=copy_password).pack(side=tk.RIGHT)
            else:
                tk.Button(frame, text="Copy (N/A)", state=tk.DISABLED).pack(side=tk.RIGHT)

def add_password():
    site = site_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    
    if not site or not user or not password:
        messagebox.showwarning("Warning", "All fields are required!")
        return
    
    cursor.execute("INSERT INTO passwords (username, website, user, password) VALUES (?, ?, ?, ?)",
                   (current_user, site, user, password))
    conn.commit()
    
    site_entry.delete(0, tk.END)
    user_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Password saved successfully!")
    display_passwords()

# GUI setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x500")

current_user = None

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack()

tk.Label(login_frame, text="Username").pack()
user_entry = tk.Entry(login_frame)
user_entry.pack()

tk.Label(login_frame, text="Password").pack()
pass_entry = tk.Entry(login_frame, show="*")
pass_entry.pack()

tk.Button(login_frame, text="Login", command=login).pack()
tk.Button(login_frame, text="Create Account", command=lambda: (login_frame.pack_forget(), reg_frame.pack())).pack()

# Registration Frame
reg_frame = tk.Frame(root)

tk.Label(reg_frame, text="New Username").pack()
reg_user_entry = tk.Entry(reg_frame)
reg_user_entry.pack()

tk.Label(reg_frame, text="New Password").pack()
reg_pass_entry = tk.Entry(reg_frame, show="*")
reg_pass_entry.pack()

tk.Button(reg_frame, text="Register", command=register).pack()
tk.Button(reg_frame, text="Back to Login", command=lambda: (reg_frame.pack_forget(), login_frame.pack())).pack()

# Main UI Frame
main_frame = tk.Frame(root)
root.mainloop()

# Close database connection on exit
conn.close()
