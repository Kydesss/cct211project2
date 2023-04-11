"""
CCT211 Project 2: Password Manager
Group 19: Joaquin Pacia, Ali Zaidi, Galad Dirie
"""

from engine import Database
from models import *
from views import *



def main():
    """
    The main function.
    """
    # Check if master password exists.
    try:
        # Checks if there is a master password file.
        with open("./data/master_password.txt", mode = "r") as master_password:
            # Checks if the master password file is empty.
            if master_password.read() == "":
                # The file is empty, so there is no master password.
                print("Master password does not exist.")
                RegisterWindow()
                ActivityLog.log(action="View register window")
            else:
                # The file probably has a master password, if not, the master password is corrupted.
                ActivityLog.log(action="View login window")
                LoginWindow()
    except:
        # The file does not exist, so there is no master password.
        print("Master password does not exist.")
        # Creates the master password file.
        with open("./data/master_password.txt", mode = "x"):
            ActivityLog.log(action='Master password file created')
        # Opens the register window.
        print("Register window opened.")
        ActivityLog.log(action='Register window opened')
        RegisterWindow()

if __name__ == "__main__":
    # Testing windows (comment out when done testing)

    # import_window = ImportWindow()
    # export_window = ExportWindow()
    # random_password_generator_window = RandomPasswordGeneratorWindow()
    # password_window = PasswordWindow()
    # database.append_password([1, 'https://google.com', 'username', 'password'])
    data_directory = "data"

    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    # Main program
    database = Database()
    PasswordVault.create_table()
    ActivityLog.create_table()


    main()
    database.close()

    


