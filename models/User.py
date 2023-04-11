from typing import List, Dict, Tuple, Union, Optional
import sqlite3
from models.base import Model
import utils.pgenerator as pg

class User(Model):
    table_name = "users"

    def __init__(self, id:int=None, username:str=None, password:str=None, role:str=None):
        self.id = id
        self.username = username
        self.password = pg.encrypt(password) # master password 
        self.role = role

    @classmethod
    def create_table(cls):
        query = f"""CREATE TABLE IF NOT EXISTS {cls.table_name} 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL)"""
        cls._execute_query(query)



#test user model
if __name__ == "__main__":

    user = User(username="test", password="test", role="admin")
    user.create_table()

    new_user = User.get_all()
    print(new_user)




