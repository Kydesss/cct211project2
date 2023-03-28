"""
CCT211 Project 2: Password Manager
Group 19: Joaquin Pacia, Ali Zaidi, Galad Dirie, Mohammed Ali
"""

# Import modules

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
