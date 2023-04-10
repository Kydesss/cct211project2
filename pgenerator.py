import random
from hashlib import sha256
from cryptography.fernet import Fernet

def create_random_password() -> str:
    """
    Creates a random password which uses a total of 15 characters with dashes (-) between 5.
    """
    i = 0
    password = ""
    while i < 17:
        if i in range(5, 19, 6):
            password += "-"
        else:
            password += base_string[random.randint(0, len(base_string) - 1)]
        i += 1
    return password

def hash(master_password: str) -> sha256:
    """
    Secures the master password.
    """
    return sha256(master_password.encode('utf-8')).hexdigest()

def verify(master_password: str) -> bool:
    """
    Checks if sha256('master_password') is the same as the locally stored master_password.
    """
    with open('master_password.txt', 'r') as f:
        stored_master_password = f.read()
    return hash(master_password) == stored_master_password
