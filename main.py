import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pyperclip

# Database setup
def init_db():
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
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

# Main Application Class
class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.conn = sqlite3.connect("passwords.db")
        self.current_user = None
        self.login_screen()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        
        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        
        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Register", command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        c = self.conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        
        if user:
            self.current_user = user[0]
            self.password_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty")
            return
        
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Account created!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def password_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Button(self.root, text="Add New Password", command=self.add_password).pack()
        tk.Button(self.root, text="Logout", command=self.logout).pack()
        
        tk.Label(self.root, text="Search:").pack()
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        tk.Button(self.root, text="Search", command=self.load_passwords).pack()
        
        self.password_frame = tk.Frame(self.root)
        self.password_frame.pack()
        self.load_passwords()

    def load_passwords(self):
        for widget in self.password_frame.winfo_children():
            widget.destroy()
        
        search_query = self.search_entry.get()
        c = self.conn.cursor()
        if search_query:
            c.execute("SELECT id, website, username, password FROM passwords WHERE user_id=? AND website LIKE ?", 
                      (self.current_user, f"%{search_query}%"))
        else:
            c.execute("SELECT id, website, username, password FROM passwords WHERE user_id=?", (self.current_user,))
        passwords = c.fetchall()
        
        for pw in passwords:
            frame = tk.Frame(self.password_frame, relief=tk.RIDGE, borderwidth=2)
            frame.pack(pady=5, fill=tk.X)
            
            tk.Label(frame, text=f"Website: {pw[1]}").pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Username: {pw[2]}").pack(side=tk.LEFT, padx=5)
            pw_label = tk.Label(frame, text="********")
            pw_label.pack(side=tk.LEFT, padx=5)
            
            def toggle_pw(label=pw_label, password=pw[3]):
                label.config(text=password if label.cget("text") == "********" else "********")
            
            def copy_pw(password=pw[3]):
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard")
            
            tk.Button(frame, text="Show", command=toggle_pw).pack(side=tk.LEFT)
            tk.Button(frame, text="Copy", command=copy_pw).pack(side=tk.LEFT)
            tk.Button(frame, text="Edit", command=lambda id=pw[0]: self.edit_password(id)).pack(side=tk.LEFT)
    
    def add_password(self):
        self.edit_password(None)
    
    def edit_password(self, pw_id):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Website:").pack()
        website_entry = tk.Entry(self.root)
        website_entry.pack()
        
        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        
        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root)
        password_entry.pack()
        
        if pw_id:
            c = self.conn.cursor()
            c.execute("SELECT website, username, password FROM passwords WHERE id=?", (pw_id,))
            pw = c.fetchone()
            if pw:
                website_entry.insert(0, pw[0])
                username_entry.insert(0, pw[1])
                password_entry.insert(0, pw[2])
        
        def save():
            website = website_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            
            if pw_id:
                self.conn.execute("UPDATE passwords SET website=?, username=?, password=? WHERE id=?", 
                                  (website, username, password, pw_id))
            else:
                self.conn.execute("INSERT INTO passwords (user_id, website, username, password) VALUES (?, ?, ?, ?)",
                                  (self.current_user, website, username, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Password saved!")
            self.password_screen()
        
        tk.Button(self.root, text="Save", command=save).pack()
        tk.Button(self.root, text="Cancel", command=self.password_screen).pack()

    def logout(self):
        self.current_user = None
        self.login_screen()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
