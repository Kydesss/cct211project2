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

import views as v # Views module
from database import Database # SQLite database module
import os # OS module
from log import Log # Activity log module

def main():
    """
    The main function.
    """
    directory = os.getcwd()
    # Check if master password exists.
    try:
        # Checks if there is a master password file.
        with open(file=directory + "\data\master_password.txt", mode = "r") as master_password:
            # Checks if the master password file is empty.
            if master_password.read() == "":
                # The file is empty, so there is no master password.
                print("Master password does not exist.")
                v.RegisterWindow(database, log)
                log.log('Register window opened')
            else:
                # The file probably has a master password, if not, the master password is corrupted.
                log.log('Login attempt')
                v.LoginWindow(database, log)
    except:
        # The file does not exist, so there is no master password.
        print("Master password does not exist.")
        # Creates the master password file.
        with open(file=directory + "\data\master_password.txt", mode = "x"):
            log.log('Master password file created')
        # Opens the register window.
        print("Register window opened.")
        log.log('Register window opened')
        v.RegisterWindow(database, log)

if __name__ == "__main__":
    # Testing windows (comment out when done testing)

    # import_window = ImportWindow()
    # export_window = ExportWindow()
    # random_password_generator_window = RandomPasswordGeneratorWindow()
    # password_window = PasswordWindow()
    # database.append_password([1, 'https://google.com', 'username', 'password'])

    # Main program
    log = Log()
    database = Database()
    main()
    database.close()
    log.close()
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Login")
        self.label = tk.Label(self.root, text = "Login")
        self.label.pack()
        self.password_label = tk.Label(self.root, text = "Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root)
        self.password_entry.pack(pady = 5)
        self.status_label = tk.Label(self.root, text = "")
        self.status_label.pack()
        self.button = tk.Button(self.root, text = 'Login', command = self.login)
        self.button.pack()
        self.root.mainloop()
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
    pass
    user = User(username="test1", password="test", role="admin")
    user.create_table()
    user.save()

    new_user = User.get_all()
    print(new_user)
