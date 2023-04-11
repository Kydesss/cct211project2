import sqlite3
from datetime import datetime
from models.base import Model

class ActivityLog(Model):
    table_name = "activity_logs"

    def __init__(self, id:int=None, session_id:int=None, action:str=None, timestamp:str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.id = id
        self.action = action
        self.timestamp = timestamp

    @classmethod
    def create_table(cls):
        #NOTE each row should be immutable, only operations should be allowed 
        print("Creating activity_logs table..")
        query = """CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            timestamp DATETIME
        )"""
        cls._execute_query(query)

    @classmethod
    def get_logs(cls):
        """Returns all activity logs with username instead of user_id"""
        query = """SELECT activity_logs.id, activity_logs.action, activity_logs.timestamp
                FROM activity_logs
                ORDER BY activity_logs.id DESC
                """
        result = cls._execute_query(query)
        return result

    @classmethod
    def log(cls, action):
        """Adds an action to the activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""INSERT INTO activity_logs ( action, timestamp)
                VALUES ( '{action}', '{timestamp}')"""
        cls._execute_query(query)

        cls(action=action, timestamp=timestamp)
        
