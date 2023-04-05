import sqlite3
from datetime import datetime
from models.base import Model

class ActivityLog(Model):
    table_name = "activity_logs"

    def __init__(self, id:int=None, user_id:int=None, action:str=None, timestamp:str=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.id = id
        self.user_id = user_id
        self.action = action
        self.timestamp = timestamp

    @classmethod
    def create_table(cls):
        #NOTE each row should be immutable, only operations should be allowed 
        query = """CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )"""
        cls._execute_query(query)

    @classmethod
    def get_logs(cls):
        """Returns all activity logs with username instead of user_id"""
        query = """SELECT activity_logs.id, users.username, activity_logs.action, activity_logs.timestamp
                   FROM activity_logs
                   JOIN users ON activity_logs.user_id = users.id
                   ORDER BY activity_logs.id DESC
                   """
        result = cls._execute_query(query)
        return result
    
    @classmethod
    def add_action(cls, user_id, action):
        """Adds an action to the activity log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"""INSERT INTO activity_logs (user_id, action, timestamp)
            VALUES ({user_id}, '{action}', '{timestamp}')
        """
        cls._execute_query(query)
        return cls(user_id=user_id, action=action, timestamp=timestamp)
