import sqlite3
import os
from models import *

class Database:

    def __init__(self) -> None:
        """
        Initializes, formats, and connects local SQLite database file.
        
        connection: Connection object to connect to SQL database for data retrival.
        """

        self.connection = self.connect()
        print("Database formatted successfully..")
        
        self.close() # TEMP setup database
    

    def connect(self):
        """
        Connects to the database.
        """
        connection = None
        #check if database exists
        try:
            with open(file="db.sql", mode="x"):
                pass
            print("Could not find database, creating new database..")
        except:
            print("Existing files found..")
        try:
            connection = sqlite3.connect("db.sql")
            print("Database connection established..")
        except sqlite3.Error as err:
            print(f"Error connecting to the database: {err}")
        return connection
            
    def close(self):
        """
        Closes the connection to the database.
        """
        self.connection.close()
        print("Database connection closed..")