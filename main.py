"""
CCT211 Project 2: Password Manager
Group 19: Joaquin Pacia, Ali Zaidi, Galad Dirie
"""

# Import modules

import tkinter as tk
from tkinter import filedialog, StringVar, ttk
import pexport as pe # Import and export CSV module
import pgenerator as pg# Password generator module
from passwordsql import Database # SQLite database module

# Initialize global database.

database = Database()

import views as v # Views module
from database import Database # SQLite database module
import os # OS module
from log import Log # Activity log module

def main():
    """
    The main function.
    """
    directory = os.getcwd()
    # Check if master password exists.
    try:
        # Checks if there is a master password file.
        with open(file=directory + "\data\master_password.txt", mode = "r") as master_password:
            # Checks if the master password file is empty.
            if master_password.read() == "":
                # The file is empty, so there is no master password.
                print("Master password does not exist.")
                v.RegisterWindow(database, log)
                log.log('Register window opened')
            else:
                # The file probably has a master password, if not, the master password is corrupted.
                log.log('Login attempt')
                v.LoginWindow(database, log)
    except:
        # The file does not exist, so there is no master password.
        print("Master password does not exist.")
        # Creates the master password file.
        with open(file=directory + "\data\master_password.txt", mode = "x"):
            log.log('Master password file created')
        # Opens the register window.
        print("Register window opened.")
        log.log('Register window opened')
        v.RegisterWindow(database, log)

if __name__ == "__main__":
    # Testing windows (comment out when done testing)

    # import_window = ImportWindow()
    # export_window = ExportWindow()
    # random_password_generator_window = RandomPasswordGeneratorWindow()
    # password_window = PasswordWindow()
    # database.append_password([1, 'https://google.com', 'username', 'password'])

    # Main program
    log = Log()
    database = Database()
    main()
    database.close()
    log.close()
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

if __name__ == "__main__":
    # Initializes and connects to the local SQLite Database.
    # database = Database()
    # import_window = ImportWindow()
    # export_window = ExportWindow()
    # random_password_generator_window = RandomPasswordGeneratorWindow()
    # database.append_password([1, 'https://google.com', 'username', 'password'])
    
    # Check if master password exists.
    # try:
    #     # Checks if there is a master password file.
    #     with open("master_password.txt", mode = "r") as master_password:
    #         # Checks if the master password file is empty.
    #         if master_password.read() == "":
    #             # The file is empty, so there is no master password.
    #             print("Master password does not exist.")
    #             register_window = RegisterWindow()
    #         else:
    #             # The file probably has a master password, if not, the master password is corrupted.
    #             login_window = LoginWindow()
    # except:
    #     # The file does not exist, so there is no master password.
    #     print("Master password does not exist.")
    #     # Creates the master password file.
    #     with open("master_password.txt", mode = "x"):
    #         pass
    #     # Opens the register window.
    #     register_window = RegisterWindow()
    pass
