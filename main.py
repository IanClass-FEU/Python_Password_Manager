import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Entry, Button
from auth import login, register_user
from password_manager import load_passwords, save_password, copy_password, edit_password
from database import init_db

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.current_user = None
        self.root.configure(bg="#2C2F33")  # Dark background
        self.login_screen()

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Username:", bg="#2C2F33", fg="white").pack()
        self.username_entry = tk.Entry(self.root, bg="#3C3F41", fg="white", insertbackground="white", highlightthickness=2, highlightbackground="white")
        self.username_entry.pack()
        
        tk.Label(self.root, text="Password:", bg="#2C2F33", fg="white").pack()
        self.password_entry = tk.Entry(self.root, show="*", bg="#3C3F41", fg="white", insertbackground="white", highlightthickness=2, highlightbackground="white")
        self.password_entry.pack()
        
        tk.Button(self.root, text="Login", command=self.try_login, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()
        tk.Button(self.root, text="Register", command=self.register_screen, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()

    def try_login(self):
        user_id = login(self.username_entry.get(), self.password_entry.get())
        if user_id:
            self.current_user = user_id
            self.password_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    def register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        fields = ["First Name:", "Middle Name (Optional):", "Last Name:", "Birthday (YYYY-MM-DD):", "Gender:", "Username:", "Password:"]
        self.entries = {}

        for field in fields:
            tk.Label(self.root, text=field, bg="#2C2F33", fg="white").pack()
            entry = tk.Entry(self.root, bg="#3C3F41", fg="white", insertbackground="white", highlightthickness=2, highlightbackground="white")
            entry.pack()
            self.entries[field] = entry

        tk.Label(self.root, text="Gender:", bg="#2C2F33", fg="white").pack()
        self.gender_var = tk.StringVar()
        gender_options = ["Male", "Female", "Other"]
        self.gender_dropdown = ttk.Combobox(self.root, textvariable=self.gender_var, values=gender_options, state="readonly")
        self.gender_dropdown.pack()

        tk.Button(self.root, text="Register", command=self.try_register, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()
        tk.Button(self.root, text="Back", command=self.login_screen, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()

    def try_register(self):
        success = register_user(
            self.entries["First Name:"].get(),
            self.entries["Middle Name (Optional):"].get(),
            self.entries["Last Name:"].get(),
            self.entries["Birthday (YYYY-MM-DD):"].get(),
            self.gender_var.get(),
            self.entries["Username:"].get(),
            self.entries["Password:"].get()
        )
        if success:
            self.login_screen()

    def password_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Button(self.root, text="Add New Password", command=self.add_password, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()
        tk.Button(self.root, text="Logout", command=self.logout, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()
        
        tk.Label(self.root, text="Search:", bg="#2C2F33", fg="white").pack()
        self.search_entry = tk.Entry(self.root, bg="#3C3F41", fg="white", insertbackground="white", highlightthickness=2, highlightbackground="white")
        self.search_entry.pack()
        tk.Button(self.root, text="Search", command=self.load_passwords, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()
        
        self.password_frame = tk.Frame(self.root, bg="#2C2F33")
        self.password_frame.pack()
        self.load_passwords()

    def load_passwords(self):
        for widget in self.password_frame.winfo_children():
            widget.destroy()
        passwords = load_passwords(self.current_user, self.search_entry.get())
        for pw in passwords:
            frame = tk.Frame(self.password_frame, relief=tk.RIDGE, borderwidth=2, bg="#2C2F33", highlightbackground="white", highlightthickness=2)
            frame.pack(pady=5, fill=tk.X)
            tk.Label(frame, text=f"Website: {pw[1]}", bg="#2C2F33", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Username: {pw[2]}", bg="#2C2F33", fg="white").pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Copy", command=lambda pw=pw[3]: copy_password(pw), bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack(side=tk.LEFT)
            tk.Button(frame, text="Show", command=lambda pw=pw[3]: messagebox.showinfo("Password", pw), bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack(side=tk.LEFT)
            tk.Button(frame, text="Edit", command=lambda pw_id=pw[0]: edit_password(pw_id), bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack(side=tk.LEFT)
    
    def add_password(self):
        add_window = Toplevel(self.root)
        add_window.title("Add New Password")
        add_window.configure(bg="#2C2F33")

        Label(add_window, text="Website:", bg="#2C2F33", fg="white").pack()
        website_entry = Entry(add_window, bg="#3C3F41", fg="white", highlightthickness=2, highlightbackground="white")
        website_entry.pack()

        Label(add_window, text="Username:", bg="#2C2F33", fg="white").pack()
        username_entry = Entry(add_window, bg="#3C3F41", fg="white", highlightthickness=2, highlightbackground="white")
        username_entry.pack()

        Label(add_window, text="Password:", bg="#2C2F33", fg="white").pack()
        password_entry = Entry(add_window, show="*", bg="#3C3F41", fg="white", highlightthickness=2, highlightbackground="white")
        password_entry.pack()

        def save_new_password():
            if website_entry.get() and username_entry.get() and password_entry.get():
                save_password(self.current_user, website_entry.get(), username_entry.get(), password_entry.get())
                messagebox.showinfo("Success", "Password saved successfully.")
                add_window.destroy()
                self.load_passwords()
            else:
                messagebox.showerror("Error", "All fields must be filled.")

        Button(add_window, text="Save", command=save_new_password, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()
        Button(add_window, text="Cancel", command=add_window.destroy, bg="#2C2F33", fg="white", borderwidth=2, highlightbackground="white").pack()

    def logout(self):
        self.current_user = None
        self.login_screen()

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
