import tkinter as tk
from tkinter import filedialog, StringVar, ttk
import utils.pexport as pe # Import and export CSV module
import utils.pgenerator as pg# Password generator module
from engine import Database
from models import *
from datetime import datetime 

# Initialize global database.

database = Database()


#TODO: Separete each window into a different file.

# UI Windows

class LoginWindow:
    """
    A window to login to the password manager.
    """
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Login")
        self.label = tk.Label(self.root, text = "Login")
        self.label.pack()
        self.password_label = tk.Label(self.root, text = "Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady = 5)
        self.status_label = tk.Label(self.root, text = "")
        self.status_label.pack()
        self.button = tk.Button(self.root, text = 'Login', command = self.login)
        self.button.pack()
        self.root.mainloop()
    
    def login(self):
        password = self.password_entry.get()
        with open("master_password.txt", mode = "r"):
            if pg.verify(password):
                print("Login successful!")
                self.root.destroy()
                PasswordWindow()
            else:
                self.status_label.config(text = "Wrong password!")

class RegisterWindow:
    """
    A window to register a master password.
    """
    def __init__(self) -> None:
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
        password = self.password_entry.get()
        with open("master_password.txt", mode = "w") as master_password:
            master_password.write(pg.hash(password))
        self.root.destroy()
        LoginWindow()

# Password Windows

class PasswordWindow:
    """
    A window to display list of passwords using a TreeView.
    """
    #TODO
    pass

class EditPasswordWindow:
    """
    A window to edit a password.
    """
    #TODO
    pass

class RandomPasswordGeneratorWindow:
    """
    A window to randomly generate a password.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.configure(state = 'readonly')
        self.password_entry.pack()
        self.button = tk.Button(self.root, text = 'Generate', command = self.create_random_password)
        self.button.pack()
        self.root.mainloop()
    
    def create_random_password(self):
        password = pg.create_random_password()
        data_string = StringVar()
        data_string.set(password)
        self.password_entry.config(textvariable = data_string)

# CSV Windows

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
            pe.import_passwords(csv_file, database)
        print("Import successful.")

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
        pe.export_passwords(database, dir_name)
        self.status_label.config(text = "Export successful.")
        print("Export Successful.")

class ActivityLogWindow:
    """
    A window to display the activity history.
    username, action, timestamp
    """

    def __init__(self) -> None:
       
        self.root = tk.Tk()
        self.root.title("Activity Log")
        self.tree = ttk.Treeview(self.root, columns=('id','username', 'action', 'timestamp'), show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('username', text='User')
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
    