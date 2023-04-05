import sqlite3
from datetime import datetime
from models.base import Model

class ActivityLogModel(Model):
    table_name = "activity_logs"

    def __init__(self, id:int=None, user_id:int=None, action:str=None, timestamp:str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.id = id
        self.user_id = user_id
        self.action = action
        self.timestamp = timestamp

    @classmethod
    def create_table(cls):
        #NOTE each row should be immutable, only operations should be allowed 
        query = """CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action text,
            timestamp text,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )"""
        cls._execute_query(query)

