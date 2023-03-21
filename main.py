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
    
    def upload():
        filename = filedialog.askopenfilename()
        print('Selected:', filename)
        with open(file=filename, mode="r") as csv_file:
            pexport.import_passwords(csv_file, database)
        print("Import successful.")
    
    root = tk.Tk()
    button = tk.Button(root, text='Import', command=upload)
    button.pack()

    root.mainloop()

class ExportWindow:
    """
    A window to export CSV files.
    """
    #TODO
    pass

if __name__ == "__main__":
    # Initializes and connects to the local SQLite Database.
    # database = Database()
    import_window = ImportWindow()
