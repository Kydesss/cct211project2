import sqlite3
from models.base import Model

class PasswordEntry(Model):
    table_name = "passwords"

    def __init__(self, id:int=None, user_id:int=None, username:str=None, password:str=None, url:str=None):
        self.id = id
        self.username = username
        self.password = password
        self.url = url
        self.user_id = user_id

    @classmethod
    def create_table(cls):
        query = f"""CREATE TABLE IF NOT EXISTS {cls.table_name} 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                url TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id))"""
        cls._execute_query(query)

    #NOTE: Should we add a method to update a password entry?
    #NOTE: We should check if there is a password entry with the same username and url before adding it. 

