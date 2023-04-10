"""
Views for the password manager.

Classes:
    LoginWindow: A window to login to the password manager.
    RegisterWindow: A window to register a master password.
    MainWindow: The main window of the password manager.
    PasswordWindow: A window to add a password to the database.
    RandomPasswordGeneratorWindow: A window to generate a random password.
    ExportWindow: A window to export the database to a CSV file.
    ImportWindow: A window to import a CSV file to the database.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from database import Database
import os
from log import Log
import utils as ut
import pandas as pd

# Global variables

directory = os.getcwd()

# Login and register windows.

class RegisterWindow:
    """
    A window to register a master password.
    """
    def __init__(self, database: Database, log: Log) -> None:
        """
        Creates a window to register a master password.
        """
        self.root = tk.Tk()
        self.root.title("Register")
        self.database = database
        self.log = log
        self.label = tk.Label(self.root, text = "Register")
        self.label.pack()
        self.password_label = tk.Label(self.root, text = "Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady = 5)
        self.button = tk.Button(self.root, text = 'Register', command = self.register)
        self.button.pack()
        self.root.mainloop()
    
    def register(self):
        """
        Registers a master password.
        """
        password = self.password_entry.get()
        with open(file = directory + "\data\master_password.txt", mode = "w") as master_password:
            master_password.write(ut.hash(password))
        self.root.destroy()
        print("Registration successful!")
        self.log.log('Registration successful')
        LoginWindow(self.database, self.log)

class LoginWindow:
    """
    A window to login to the password manager.
    """
    def __init__(self, database: Database, log: Log) -> None:
        """
        Creates a window to login to the password manager.
        """
        self.root = tk.Tk()
        self.root.title("Login")
        self.database = database
        self.log = log
        self.label = tk.Label(self.root, text = "Login")
        self.label.pack()
        self.password_label = tk.Label(self.root, text = "Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady = 5)
        self.button = tk.Button(self.root, text = 'Login', command = self.login)
        self.button.pack()
        self.status_label = tk.Label(self.root, text = "")
        self.status_label.pack()
        self.root.mainloop()
    
    def login(self):
        """
        Logs in to the password manager.
        """
        password = self.password_entry.get()
        with open(file = directory + "\data\master_password.txt", mode = "r"):
            if ut.verify(password):
                self.root.destroy()
                print("Login successful!")
                self.log.log('Login successful')
                PasswordWindow(self.database, self.log)
            else:
                self.log.log('Wrong password')
                self.status_label.config(text = "Wrong password!")

# Password Windows

class PasswordWindow:
    """
    A window to display list of passwords using a TreeView.
    """
    def __init__(self, database: Database, log: Log) -> None:
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.database = database
        self.log = log
        self.menu = tk.Menu(self.root, tearoff = 0)
        self.menu.add_command(label = "Add Password", command = self.add_password)
        self.menu.add_command(label = "Edit Password", command = self.edit_password)
        self.menu.add_command(label = "Delete Password", command = self.delete_password)
        self.menu.add_command(label = "Generate Password", command = self.generate_password)
        self.menu.add_command(label = "Import Passwords", command = self.import_passwords)
        self.menu.add_command(label = "Export Passwords", command = self.export_passwords)
        self.menu.add_separator()
        self.menu.add_command(label = "Sign Out", command = self.sign_out)
        self.menu.add_command(label = "Exit", command = self.root.destroy)
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("id", "url", "username", "password")
        self.tree.column("#0", width = 0, stretch = tk.NO)
        self.tree.column("id", anchor = tk.W, width = 30)
        self.tree.column("url", anchor = tk.W, width = 150)
        self.tree.column("username", anchor = tk.W, width = 150)
        self.tree.column("password", anchor = tk.W, width = 150)
        self.tree.heading("#0", text = "id", anchor = tk.W)
        self.tree.heading("id", text = "ID", anchor = tk.W)
        self.tree.heading("url", text = "URL", anchor = tk.W)
        self.tree.heading("username", text = "Username", anchor = tk.W)
        self.tree.heading("password", text = "Password", anchor = tk.W)
        self.tree.pack()
        self.refresh_tree()
        self.root.config(menu = self.menu)
        self.root.mainloop()
    
    def add_password(self) -> None:
        """
        Opens an edit window to add a password.
        """
        AddPasswordWindow(self)
    
    def edit_password(self) -> None:
        """
        Opens an edit window to edit a password.
        """
        selected = self.tree.selection()[0]
        selected = self.tree.item(selected, "values")
        EditPasswordWindow(self, selected)
    
    def delete_password(self) -> None:
        """
        Deletes a password from the database.
        """
        selected = self.tree.selection()[0]
        entry = self.tree.item(selected, "values")
        id = entry[0]
        url = entry[1]
        username = entry[2]
        password = entry[3]
        self.database.delete_query(id)
        self.refresh_tree()
        print("Password deleted. " + str(entry))
        self.log.log("Deleted password for", url, username, password)
    
    def generate_password(self) -> None:
        """
        Opens a window to generate a password.
        """
        self.log.log("Opened password generator")
        RandomPasswordGeneratorWindow()
    
    def import_passwords(self) -> None:
        """
        Opens a file dialog to import passwords from a CSV file.
        """
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        with open(file=filename, mode = "r") as csv_file:
            self.database.import_passwords(csv_file)
        self.refresh_tree()
        print("Import successful.")
        action = "Imported passwords from " + filename
        self.log.log(action)

    def export_passwords(self) -> None:
        """
        Opens a file dialog to export passwords to a CSV file.
        """
        data = self.database.read_query()
        for i in range(len(data)):
            data[i] = (data[i][1], data[i][1], data[i][2], ut.decrypt(data[i][3]))
        df = pd.DataFrame(data, columns=["name", "url", "username", "password"])
        filename = filedialog.asksaveasfile(initialfile = 'local_passwords.csv',
        defaultextension=".csv", filetypes=[("csv file","*.csv*")])
        df.to_csv(filename, sep = ",", index = False)
        print("Export successful.")
        action = "Exported passwords to " + filename.name
        self.log.log(action)
    
    def sign_out(self) -> None:
        """
        Signs out of the current account.
        """
        self.root.destroy()
        print("Signed out successfully!")
        self.log.log("Signed out")
        LoginWindow(self.database, self.log)
    
    def refresh_tree(self) -> None:
        """
        Refreshes the TreeView to update the passwords.
        """
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in self.database.read_query():
            self.tree.insert("", tk.END, values = (i[0], i[1], i[2], ut.decrypt(i[3])))

class AddPasswordWindow:
    """
    A window to add a password.
    """
    def __init__(self, parent: PasswordWindow) -> None:
        """
        Initializes the window.
        """
        self.parent = parent
        self.root = tk.Tk()
        self.root.title("Add Password")
        self.url_label = tk.Label(self.root, text = "URL")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack(pady = 5)
        self.username_label = tk.Label(self.root, text = "Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady = 5)
        self.password_label = tk.Label(self.root, text = "Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady = 5)
        self.button = tk.Button(self.root, text = 'Save', command = self.add)
        self.button.pack()
        self.root.mainloop()
    
    def add(self):
        """
        Adds the password to the database.
        """
        url = self.url_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.parent.database.append_password([0, url, username, password]) # Append the password to the database.
        self.parent.log.log("Added password for", url, username, password)
        self.parent.refresh_tree() # Refresh the tree.
        self.root.destroy()
        print("Password added.")
        

class EditPasswordWindow:
    """
    A window to edit a password.
    """
    def __init__(self, parent: PasswordWindow, selected) -> None:
        """
        Initializes the window.
        """
        self.root = tk.Tk()
        self.root.title("Edit Password")
        self.parent = parent
        self.selected = selected
        self.url_label = tk.Label(self.root, text = "URL")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack(pady = 5)
        self.username_label = tk.Label(self.root, text = "Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady = 5)
        self.password_label = tk.Label(self.root, text = "Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady = 5)
        self.add_selected() # Add the selected password to the Entry boxes.
        self.button = tk.Button(self.root, text = 'Save', command = self.edit)
        self.button.pack()
        self.root.mainloop()
    
    def add_selected(self):
        """
        Adds the selected password to the Entry boxes.
        """
        self.url_entry.insert(0, self.selected[1])
        self.username_entry.insert(0, self.selected[2])
        self.password_entry.insert(0, self.selected[3])
    
    def edit(self):
        """
        Edits the password in the database.
        """
        id = self.selected[0]
        url = self.url_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.parent.database.edit_query(id, url, username, ut.encrypt(password)) # Edit the password in the database.
        self.parent.log.log("Edited password for", url, username, password)
        self.parent.refresh_tree() # Refresh the tree.
        self.root.destroy()
        print("Password edited.")
        

# Random Password Generator Window

class RandomPasswordGeneratorWindow:
    """
    A window to randomly generate a password.
    """

    def __init__(self) -> None:
        """
        Initializes the window.
        """
        self.root = tk.Tk()
        self.root.title("Random Password Generator")
        self.password_entry = tk.Text(self.root, height=1, width=17, font=("Helvetica", 11))
        self.password_entry.pack()
        self.button = tk.Button(self.root, text = 'Generate', command = self.create_random_password)
        self.button.pack()
        self.root.mainloop()
    
    def create_random_password(self):
        """
        Creates a random password.
        """
        password = ut.create_random_password()
        self.password_entry.delete(1.0, tk.END)
        self.password_entry.insert(1.0, password)
        print("Password generated.")