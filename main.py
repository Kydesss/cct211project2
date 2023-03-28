"""
CCT211 Project 2: Password Manager
Group 19: Joaquin Pacia, Ali Zaidi, Galad Dirie, Mohammed Ali
"""

# Import modules
import tkinter as tk
from tkinter import filedialog # Import or export files.
import random # Random password generator.
import sqlite3 # Database.

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
    #TODO
    pass

class ExportWindow:
    """
    A window to export CSV files.
    """
    #TODO
    pass

# Database

class Database:
    """
    A class to connect to the SQLite database.
    """
    #TODO
    pass

if __name__ == "__main__":

    # Initializes and connects to the local SQLite Database.
    database = Database()

    # Creates the login window.
    login_window = LoginWindow()
