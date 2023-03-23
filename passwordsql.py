"""
Creates a custom SQLite database with additional features.

database.read_query reads the data in the database and returns a list[tuple].
database.insert_password(entry: list) inserts a password entry as a list.
database.delete_query(id: int) deletes a password in the database according to the id number.
database.execute_query(query: str) executes an SQLite format query to change the database.

"""

import sqlite3
import os
from sqlite3 import Error

# https://www.freecodecamp.org/news/connect-python-with-sql/

class Database():

    def __init__(self) -> None:
        """
        Initializes, formats, and connects local SQLite database file.
        
        connection: Connection object to connect to SQL database for data retrival.
        """
        try:
            with open(file="passwords.sql", mode="x"):
                pass
            print("Could not find files, creating new files..")
        except:
            print("Existing files found..")
        directory = os.getcwd()
        try:
            self.connection = sqlite3.connect(directory + "\passwords.sql")
            print("Local connection established..")
            cursor = self.connection.cursor()
            query = """CREATE TABLE IF NOT EXISTS passwords 
            (id INT PRIMARY KEY NOT NULL, 
            url TEXT NOT NULL, 
            username TEXT NOT NULL, 
            password TEXT NOT NULL);"""
            cursor.execute(query)
            print("Database formatted successfully..")
        except Error as err:
            print(f"Error: '{err}'")
        
    def read_query(self) -> list[tuple]:
        """
        Reads the SQLite database and returns a list of passwords.
        """
        query = """SELECT * FROM passwords"""
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")
    
    def insert_password(self, entry: list[str]):
        """
        Inserts a password into the SQLite database.
        """
        url = entry[1]
        username = entry[2]
        password = entry[3]
        id = self.read_query()
        if id == []:
            id = 1
        else:
            id = len(id) + 1
        append_password = f"""INSERT INTO passwords VALUES ({id}, \'{url}\', \'{username}\', \'{password}\')"""
        self.execute_query(append_password)

    def delete_query(self, id: int):
        """
        Deletes a password from the database.
        """
        delete = f"""DELETE FROM passwords WHERE id = {str(id)};"""
        self.execute_query(delete)

    def execute_query(self, query):
        """
        Commits queries to the SQLite database
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as err:
            print(f"Error: '{err}'")