"""
Creates a custom SQLite database with additional features.

Database.read_query() reads the data in the database and returns a list[tuple], tuple(id: int, url: str, username: str, password: str).
Database.append_password(entry: list) appends a password entry as a list.
Database.delete_query(id: int) deletes a password in the database according to the id number.
Database.execute_query(query: str) executes an SQLite format query to change the database.
Database.close() closes the connection to the database.
"""

import sqlite3
import os
from sqlite3 import Error
import utils as ut
import csv

# https://www.freecodecamp.org/news/connect-python-with-sql/

class Database():

    def __init__(self) -> None:
        """
        Initializes, formats, and connects a local SQLite database file.
        
        connection: Connection object to connect to SQL database for data retrival.
        """
        try:
            with open(file="passwords.sql", mode="x"):
                pass
            print("Could not find database, creating new database..")
        except:
            print("Existing files found..")
        directory = os.getcwd()
        try:
            self.connection = sqlite3.connect(directory + "\passwords.sql")
            print("Database connected..")
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
        list[tuple]: [(id, url, username, password)]
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
    
    def append_password(self, entry: list[int, str, str, str]):
        """
        Inserts a password into the SQLite database.
        entry: [id, url, username, password]
        """
        url = entry[1]
        username = entry[2]
        password = ut.encrypt(entry[3]) # Automatically encrypts password.
        id = self.read_query()
        if id == []:
            id = 1
        else:
            id = id[len(id) - 1][0] + 1
        append_password = f"""INSERT INTO passwords VALUES ({id}, \'{url}\', \'{username}\', \'{password}\')"""
        self.execute_query(append_password)

    def delete_query(self, id: int):
        """
        Deletes a password from the database.
        """
        delete = f"""DELETE FROM passwords WHERE id = {str(id)};"""
        self.execute_query(delete)
    
    def edit_query(self, id: int, url: str, username: str, password: str):
        """
        Edits a password in the database.
        """
        edit = f"""UPDATE passwords SET url = \'{url}\', username = \'{username}\', password = \'{password}\' WHERE id = {id}"""
        self.execute_query(edit)

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
    
    def import_passwords(self, passwords: csv):
        """
        Imports CSV password files from Chrome or Edge.
        """
        csv_reader = csv.reader(passwords)
        list_of_passwords = []
        for row in csv_reader:
            list_of_passwords.append(row)
        list_of_passwords.pop(0)
        for i in list_of_passwords:
            self.append_password(i)
    
    def export_passwords(self) -> csv:
        """
        Exports passwords from SQLite database to a CSV file.
        """
        read_database = self.read_query()
        export = [['name', 'url', 'username', 'password']]
        for entry in read_database:
            single_entry = []
            i = 0
            for col in entry:
                if i == 3:
                    col = ut.decrypt(col)
                single_entry.append(col)
                i += 1
            single_entry[0] = entry[1]
            export.append(single_entry)
        with open(file='passwords.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(export)
        
    def close(self):
        """
        Closes the connection to the SQLite database.
        """
        self.connection.close()
        print("Database connection closed..")