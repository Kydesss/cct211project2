"""
CCT211 Project 2: Password Manager
Group 19: Joaquin Pacia, Ali Zaidi, Galad Dirie
"""
import uuid
import socket
import platform
from datetime import datetime 


from engine import Database
from models import *
from views import *



#initlize models
def init_models():
    User.create_table()
    PasswordEntry.create_table()
    ActivityLog.create_table()

 
class SessionManager:
    def __init__(self):
        self.user = None
        self.actions = []
        self.start_time = datetime.now()
        self.end_time = None
        self.ip_address = self._get_ip_address()
        self.device_info = self._get_device_info()
        
    def _get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def _get_device_info(self):
        return platform.uname()

    def start(self):
        self.start_time = datetime.now()
        Session.create(user_id=self.user.id, start_time=self.start_time, ip_address=self.ip_address, device_info=self.device_info)

    def set_user(self, user):
        self.user = user

    def add_action(self, action, timestamp):
        self.actions.append((action, timestamp))
        database.activity_log_table.add_action(self.user, action, timestamp)

    def get_actions(self):
        return self.actions
    
    def close(self):
        self.end_time = datetime.now()
        self.add_action("logout", self.end_time)
        self.save()



class Main:
    """handles the main loop of the application
    creates views and passes them the session manager

    """

    def __init__(self):
        self.database = Database()
        self.session = SessionManager()
        self.login_window = LoginWindow(self)

    def login(self, username, password):
       ...
    
    def register(self, username, password):
        ...
    

if __name__ == "__main__":
    # Initializes and connects to the local SQLite Database.
    # database = Database()
    # print(database.connection)
    # # import_window = ImportWindow()
    # # export_window = ExportWindow()

    # user = UserModel.create_user("admin", "test", "super_user")

    # activity_log_window = ActivityLogWindow()
    # # random_password_generator_window = RandomPasswordGeneratorWindow()
    # database.append_password([1, 'https://google.com', 'username', 'password'])
    
    # Check if master password exists.
    # try:
    #     # Checks if there is a master password file.
    #     with open("master_password.txt", mode = "r") as master_password:
    #         # Checks if the master password file is empty.
    #         if master_password.read() == "":
    #             # The file is empty, so there is no master password.
    #             print("Master password does not exist.")
    #             register_window = RegisterWindow()
    #         else:
    #             # The file probably has a master password, if not, the master password is corrupted.
    #             login_window = LoginWindow()
    # except:
    #     # The file does not exist, so there is no master password.
    #     print("Master password does not exist.")
    #     # Creates the master password file.
    #     with open("master_password.txt", mode = "x"):
    #         pass
    #     # Opens the register window.
    #     register_window = RegisterWindow()

    init_models()
    try:
    
        user = User(username="test1", password="test", role="admin")
        user.save()
    except:
        pass
        
    new_user = User.get_all()

    # add activity log
    activity_log = ActivityLog(user_id=1, action="login", timestamp=datetime.now())
    activity_log.save()

    #activity window
    activity_log_window = ActivityLogWindow()

    
    print(new_user)
