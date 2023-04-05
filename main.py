"""
CCT211 Project 2: Password Manager
Group 19: Joaquin Pacia, Ali Zaidi, Galad Dirie, Mohammed Ali
"""

# Import modules

import views as v # Views module
from database import Database # SQLite database module

def main():
    """
    The main function.
    """
    # Check if master password exists.
    try:
        # Checks if there is a master password file.
        with open("master_password.txt", mode = "r") as master_password:
            # Checks if the master password file is empty.
            if master_password.read() == "":
                # The file is empty, so there is no master password.
                print("Master password does not exist.")
                v.RegisterWindow(database)
            else:
                # The file probably has a master password, if not, the master password is corrupted.
                v.LoginWindow(database)
    except:
        # The file does not exist, so there is no master password.
        print("Master password does not exist.")
        # Creates the master password file.
        with open("master_password.txt", mode = "x"):
            pass
        # Opens the register window.
        print("Register window opened.")
        v.RegisterWindow(database)

if __name__ == "__main__":
    # Testing windows (comment out when done testing)

    # import_window = ImportWindow()
    # export_window = ExportWindow()
    # random_password_generator_window = RandomPasswordGeneratorWindow()
    # password_window = PasswordWindow()
    # database.append_password([1, 'https://google.com', 'username', 'password'])

    # Main program
    database = Database()
    main()
    database.close()