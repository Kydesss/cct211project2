"""
CCT211 Project 2: Password Manager
Group 19: Joaquin Pacia, Ali Zaidi, Galad Dirie
"""

# Import modules
import tkinter as tk
from tkinter import filedialog
import pexport # Import and export CSV module
import pgenerator # Password generator module
from passwordsql import Database # SQLite database module

database = Database()
# UI Windows

class LoginWindow:
    """
    A window to login to the password manager.
    """
    #TODO
    pass

class DashboardWindow:
    """
    A window to access the dashboard.
    """
    #TODO
    pass

# Password Windows

class PasswordWindow:
    """
    A window to display list of passwords.
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
    #TODO
    pass

# CSV Windows

class ImportWindow:
    """
    A window to import CSV files.
    """

    def __init__(self) -> None:
        root = tk.Tk()
        button = tk.Button(root, text='Import', command=self.upload)
        button.pack()
        root.mainloop()
    
    def upload(self):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        with open(file=filename, mode="r") as csv_file:
            pexport.import_passwords(csv_file, database)
        print("Import successful.")

class ExportWindow:
    """
    A window to export CSV files.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.label = tk.Label(self.root, text='Write the name of file')
        self.label.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.button = tk.Button(self.root, text='Export', command=self.export)
        self.button.pack()
        self.root.mainloop()

    def export(self):
        filename = self.entry.get()
        dir_name = filedialog.askdirectory() + f'\{filename}' + ".csv"
        pexport.export_passwords(database, dir_name)
        print("Export Successful.")

if __name__ == "__main__":
    # Initializes and connects to the local SQLite Database.
    # database = Database()
    export_window = ExportWindow()
