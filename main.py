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



# Initialize global database.

 
class Session:
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
        # add session to session table
        database.session_table.add_session(self.start_time, self.ip_address, self.device_info)

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
    loads the database
    loads the session manager
    loads the login window
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
    user = User(username="test1", password="test", role="admin")
    user.create_table()
    user.save()

    new_user = User.get_all()
    print(new_user)
