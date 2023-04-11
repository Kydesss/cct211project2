#defines Session Model in sqlite3 database

import sqlite3
from models.base import Model

class Session(Model):
    table_name = "sessions"
    
    def __init__(self, id:int=None, user_id:int=None, activity_log_id:int=None, start_time:str=None, end_time:str=None, ip_address:str=None, device_info:str=None):
        self.id = id
        self.user_id = user_id
        self.activity_log_id = activity_log_id
        self.start_time = start_time
        self.end_time = end_time
        self.ip_address = ip_address
        self.device_info = device_info
    
    @classmethod
    def create_table(cls):
        query = """CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_log_id INTEGER,
            start_time text,
            end_time text,
            ip_address text,
            device_info text,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (activity_log_id) REFERENCES activity_log (id)
        )"""
        cls._execute_query(query)
