"""
Creates a SQLite database for logging actions.

Log.log(action: str, url=None, username=None, password=None) logs an action to the SQLite database.
Log.close() closes the connection to the SQLite database.
"""

import sqlite3
import os
from sqlite3 import Error
import datetime

class Log():

    def __init__(self) -> None:
        directory = os.getcwd()
        try:
            with open(file=directory + "\data\log.sql", mode="x"):
                pass
            print("Could not find activity log database, creating new database..")
        except:
            print("Existing log found..")
        
        try:
            self.connection = sqlite3.connect(directory + "\data\log.sql")
            print("Activity log database connected..")
            cursor = self.connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS log
            (action TEXT NOT NULL, date DATETIME NOT NULL);"""
            cursor.execute(query)
            self.log('Successfully connected to log')
        except Error as err:
            print(f"Error: '{err}'")
    
    def log(self, action: str, url=None, username=None, password=None):
        """
        Logs an action to the SQLite database.
        """
        if url != None and username != None and password != None:
            action = f"{action} {url}"
        cursor = self.connection.cursor()
        query = f"INSERT INTO log VALUES ('{action}', '{datetime.datetime.today().replace(microsecond=0)}');"
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as err:
            print(f"Error: '{err}'")
    
    def read_log(self) -> list[tuple]:
        """
        Reads the log.
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM log;"
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as err:
            print(f"Error: '{err}'")
    
    def close(self):
        """
        Closes the connection to the Log.
        """
        self.connection.close()
        print("Log connection closed..")