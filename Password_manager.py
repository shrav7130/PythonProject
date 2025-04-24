import tkinter as tk
from tkinter import messagebox
import json
from tkinter import ttk

class PasswordManager:
    def __init__(self, master, master_password):
        self.master = master
        
        self.master.option_add("*Font", "Helvetica 14")
        self.master.option_add("*Entry.Font", "Helvetica 14")
        self.master.option_add("*Button.Font", "Helvetica 14")
        self.master.option_add("*Label.Font", "Helvetica 14")
        self.master.option_add("*Treeview.Heading.Font", "Helvetica 14 bold")
        self.master.option_add("*Treeview.Font", "Helvetica 13")
    
        self.master.title("Password Manager")
        self.master.geometry("800x600")
        self.master_password = master_password
        self.passwords = {}
        
        self.load_passwords() # it will load passwords from the file (if it exists)

        self.bg_color = "light blue"
        self.master.config(bg=self.bg_color)
 
        self.label_login = tk.Label(master, text="Enter Master Password:", bg=self.bg_color)
        self.label_login.pack()

        self.master_password_entry = tk.Entry(master, show="*", bg=self.bg_color)
        self.master_password_entry.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login, bg=self.bg_color)
        self.login_button.pack()

    def login(self):
        entered_password = self.master_password_entry.get()

        if entered_password == self.master_password:
            self.master_password_entry.pack_forget()
            self.login_button.pack_forget()

            
            self.label_login.pack_forget()
            self.label_action = tk.Label(self.master, text="Choose an action:", bg=self.bg_color)
            self.label_action.pack()

            self.add_button = tk.Button(self.master, text="Add Password", command=self.show_add_pass, bg=self.bg_color)
            self.add_button.pack()

            self.view_button = tk.Button(self.master, text="View Passwords", command=self.view_pass, bg=self.bg_color)
            self.view_button.pack()

        else:
            messagebox.showwarning("Error", "Invalid Master Password")

    def show_add_pass(self):
        
        self.clear_widgets()

        self.label_website = tk.Label(self.master, text="Enter website:")
        self.label_website.pack()

        self.website_entry = tk.Entry(self.master)
        self.website_entry.pack()

        self.label_username = tk.Label(self.master, text="Enter username:")
        self.label_username.pack()

        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.label_password = tk.Label(self.master, text="Enter password:")
        self.label_password.pack()

        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.strength_label = tk.Label(self.master, text="", fg="red")
        self.strength_label.pack()

        self.password_entry.bind("<KeyRelease>", self.on_pass_change)

        self.save_button = tk.Button(self.master, text="Save Password", command=self.save_password)
        self.save_button.pack()

    def view_pass(self):
        
        self.clear_widgets()

        self.tree = ttk.Treeview(self.master, columns=("website", "username", "password"), show="headings")
        self.tree.heading("website", text="Website")
        self.tree.heading("username", text="Username")
        self.tree.heading("password", text="Password")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

        self.tree.tag_configure("large_font", font=("Helvetica", 12))   # it will Set larger font size for the Treeview contents

        for website, password_info in self.passwords.items():
            username = password_info["username"]
            password = password_info["password"]
            self.tree.insert("", tk.END, values=(website, username, password), tags="large_font")

        self.tree.pack(expand=True, fill="both", padx=20, pady=20)
        
        
        # Right-click menu
        self.menu = tk.Menu(self.master, tearoff=0)
        self.menu.add_command(label="Copy Username", command=lambda: self.copy_item(0))
        self.menu.add_command(label="Copy Password", command=lambda: self.copy_item(1))

        # Bind right-click to show the menu
        def on_right_click(event):
            row_id = self.tree.identify_row(event.y)
            if row_id:
                self.tree.selection_set(row_id)
                self.menu.post(event.x_root, event.y_root)

        self.tree.bind("<Button-3>", on_right_click)

        # Add a Back button
        self.back_button = tk.Button(self.master, text="Back", command=self.show_main_menu, bg=self.bg_color)
        self.back_button.pack(pady=10)

    
    def copy_item(self, col_index):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            value = item["values"][col_index+1]
            self.master.clipboard_clear()
            self.master.clipboard_append(value)
            self.master.update()

    #After clicking back button this menu will appears    
    def show_main_menu(self):
        self.clear_widgets()

        self.label_action = tk.Label(self.master, text="Choose an action:", bg=self.bg_color)
        self.label_action.pack()

        self.add_button = tk.Button(self.master, text="Add Password", command=self.show_add_pass, bg=self.bg_color)
        self.add_button.pack()

        self.view_button = tk.Button(self.master, text="View Passwords", command=self.view_pass, bg=self.bg_color)
        self.view_button.pack()

        self.quit_button = tk.Button(self.master, text="Quit", command=self.master.destroy, bg=self.bg_color)
        self.quit_button.pack()

    def on_pass_change(self, event):
        password = self.password_entry.get()
        strength = self.check_pass_strength(password)
        self.strength_label.config(text=f"Password Strength: {strength}", fg=self.get_strength_color(strength))

    def check_pass_strength(self, password):
    
        length = len(password)
        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)

        if length >= 8 and has_uppercase and has_lowercase and has_digit:
            return "Strong"
        elif length >= 6 and (has_uppercase or has_lowercase) and has_digit:
            return "Moderate"
        else:
            return "Weak"

    def get_strength_color(self, strength):
        if strength == "Strong":
            return "green"
        elif strength == "Moderate":
            return "orange"
        else:
            return "red"

    def save_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            self.passwords[website] = {"username": username, "password": password}
            self.save_passwords_to_file()  
            messagebox.showinfo("Success", "Password saved successfully!")

            
            self.clear_widgets()
            self.label_action.pack()

            self.view_button = tk.Button(self.master, text="View Passwords", command=self.view_pass)
            self.view_button.pack()

            self.quit_button = tk.Button(self.master, text="Quit", command=self.master.destroy)
            self.quit_button.pack()

        else:
            messagebox.showwarning("Error", "Please enter website, username, and password.")

    


    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

    def save_passwords_to_file(self):
        with open("passwords.json", "w") as file:
            json.dump(self.passwords, file)

    def load_passwords(self):
        try:
            with open("passwords.json", "r") as file:
                self.passwords = json.load(file)
        except FileNotFoundError:
            self.passwords = {}

root = tk.Tk()
root.geometry("400x300")

master_password = "pass"
app = PasswordManager(root, master_password)

root.mainloop()
