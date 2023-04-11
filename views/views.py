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
import os
import utils as ut
from models import *
import pandas as pd



# Global variables

directory = os.getcwd()

# Login and register windows.

class RegisterWindow:
    """
    A window to register a master password.
    """
    def __init__(self) -> None:
        """
        Creates a window to register a master password.
        """
        self.root = tk.Tk()
        self.root.title("Register")
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
        with open(file = directory + "/data/master_password.txt", mode = "w") as master_password:
            master_password.write(ut.hash(password))
        self.root.destroy()
        print("Registration successful!")
        ActivityLog.log('Registration successful')
        LoginWindow()


class LoginWindow:
    """
    A window to login to the password manager.
    """
    def __init__(self) -> None:
        """
        Creates a window to login to the password manager.
        """
        self.root = tk.Tk()
        self.root.title("Login")
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
                ActivityLog.log('Login successful')
                PasswordWindow()
            else:
                ActivityLog.log('Wrong login password')
                self.status_label.config(text = "Wrong password!")

# Password Windows

class PasswordWindow:
    """
    A window to display list of passwords using a TreeView.
    """
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.menu = tk.Menu(self.root, tearoff = 0)
        self.menu.add_command(label = "Add Password", command = self.add_password)
        self.menu.add_command(label = "Edit Password", command = self.edit_password)
        self.menu.add_command(label = "Delete Password", command = self.delete_password)
        self.menu.add_command(label = "Generate Password", command = self.generate_password)
        self.menu.add_command(label = "Import Passwords", command = self.import_passwords)
        self.menu.add_command(label = "Export Passwords", command = self.export_passwords)
        self.menu.add_separator()
        self.menu.add_command(label = "View Activity Log", command = self.view_log)
        self.menu.add_command(label = "Delete All Passwords", command = self.delete_all_passwords)
        self.menu.add_command(label = "Sign Out", command = self.sign_out)
        self.menu.add_command(label = "Exit", command = self.root.destroy)
        self.tree = ttk.Treeview(self.root, columns= ("id", "url", "username", "password"), show = "headings")
        self.tree.heading("#0", text = "id", anchor = tk.W)
        self.tree.heading("id", text = "ID", anchor = tk.W)
        self.tree.heading("url", text = "URL", anchor = tk.W)
        self.tree.heading("username", text = "Username", anchor = tk.W)
        self.tree.heading("password", text = "Password", anchor = tk.W)

        self.tree.column("#0", width = 0, stretch = tk.NO)
        self.tree.column("id", anchor = tk.W, width = 30)
        self.tree.column("url", anchor = tk.W, width = 150)
        self.tree.column("username", anchor = tk.W, width = 150)
        self.tree.column("password", anchor = tk.W, width = 150)
        
        self.tree.pack(expand=True, fill='both')
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
        PasswordVault.delete_password(id)
        self.refresh_tree()
        print("Password deleted. " + str(entry))
        action = "Deleted password for " + url + " with username " + username + " and password " + password
        ActivityLog.log(action)
    
    def delete_all_passwords(self) -> None:
        """
        Deletes all passwords from the database.
        """
        DeletePasswordWindow(self)
              
    def generate_password(self) -> None:
        """
        Opens a window to generate a password.
        """
        ActivityLog.log("Opened password generator")
        RandomPasswordGeneratorWindow()
     
    def view_log(self) -> None:
        """
        Opens a window to view the activity log.
        """
        ActivityLog.log("Opened activity log")
        ActivityLogWindow()

    def import_passwords(self):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        with open(file=filename, mode = "r") as csv_file:
            PasswordVault.import_passwords(csv_file)
        self.refresh_tree()
        print("Import successful.")
        action = "Imported passwords from " + filename
        ActivityLog.log(action)

    def export_passwords(self):
        filename = filedialog.asksaveasfile(initialfile = 'local_passwords.csv',
        defaultextension=".csv", filetypes=[("csv file","*.csv*")])
        PasswordVault.export_passwords(filename.name)
        print("Export successful.")
        action = "Exported passwords to " + filename.name
        ActivityLog.log(action)
    
    def sign_out(self) -> None:
        """
        Signs out of the current account.
        """
        self.root.destroy()
        print("Signed out successfully!")
        ActivityLog.log("Signed out")
        LoginWindow()
    
    def refresh_tree(self) -> None:
        """
        Refreshes the TreeView to update the passwords.
        """
        pm = ut.passwordM()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i in PasswordVault.get_passwords():
            print(i)
            self.tree.insert("", tk.END, values = (i[0], i[1], i[2], ut.decrypt(password=i[3])))


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
        PasswordVault.add_password(username, password, url)
        ActivityLog.log(action=f"Added password for {url} with username {username}")
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
        PasswordVault.update(id=id, url=url, username=username, password=password)
        ActivityLog.log("Edited password for", url, username, password)
        self.parent.refresh_tree() # Refresh the tree.
        self.root.destroy()
        print("Password edited.")    


class DeletePasswordWindow:
    """
    A window to delete a password.
    """
    def __init__(self, parent: PasswordWindow) -> None:
        """
        Initializes the window.
        """
        self.root = tk.Tk()
        self.root.title("Delete All Passwords")
        self.parent = parent
        self.label = tk.Label(self.root, text = "Are you sure you want to delete all passwords?")
        self.label.pack()
        self.button = tk.Button(self.root, text = 'Delete', command = self.delete)
        self.button.pack()
        self.root.mainloop()
    
    def delete(self):
        """
        Deletes all passwords.
        """
        PasswordVault.delete_all()
        self.parent.refresh_tree()
        print("All passwords deleted.")
        ActivityLog.log("Deleted all passwords.")
        self.root.destroy()

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


class ImportWindow:
    """
    A window to import CSV files.
    """

    def __init__(self) -> None:
        root = tk.Tk()
        button = tk.Button(root, text = 'Import', command = self.upload)
        button.pack()
        root.mainloop()
    
    def upload(self):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        with open(file=filename, mode = "r") as csv_file:
            PasswordVault.import_passwords(csv_file)
        print("Import successful.")
        action = "Imported passwords from " + filename
        ActivityLog.log(action)


class ExportWindow:
    """
    A window to export CSV files.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.label = tk.Label(self.root, text = 'What do you want to name your file?')
        self.label.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.button = tk.Button(self.root, text = 'Export', command=self.export)
        self.button.pack()
        self.status_label = tk.Label(self.root, text = '')
        self.status_label.pack()
        self.root.mainloop()

    def export(self):
        filename = self.entry.get()
        dir_name = filedialog.askdirectory() + f'\{filename}' + ".csv"
        PasswordVault.export_passwords(dir_name)
        self.status_label.config(text = "Export successful.")
        print("Export Successful.")
        action = "Exported passwords to " + dir_name
        ActivityLog.log(action)


# Log Window

class ActivityLogWindow:
    """
    A window to display the activity history.
    username, action, timestamp
    """

    def __init__(self) -> None:
       
        self.root = tk.Tk()
        self.root.title("Activity Log")
        self.tree = ttk.Treeview(self.root, columns=('id', 'action', 'timestamp'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('action', text='Action')
        self.tree.heading('timestamp', text='Timestamp')
        self.tree.pack(expand=True, fill='both')
        self.update_log()
        self.root.mainloop()

    def update_log(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        activity_log = self.get_activity_log()
        for entry in activity_log:
            self.tree.insert('', 'end', values=entry)

    def get_activity_log(self):
        #return list of tuples (action, timestamp)
        return ActivityLog.get_logs()
    

    