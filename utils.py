"""
This file contains all the functions that are used in the main.py file.

Functions:
    create_random_password() -> str - Creates a random password which uses a total of 15 characters with dashes (-) between 5.
    encrypt(password: str) -> str - Encrypts 'password' using our custom encryption algorithm.
    decrypt(password: str) -> str - Decrypts 'password' using our custom encryption algorithm.
    hash_password(password: str) -> str - Hashes 'password' using SHA256.
    verify(password: str) -> bool - Verifies if 'password' matches 'hashed_password'.

"""

import random
from hashlib import sha256
import os
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode # Base64 module

key = Fernet.generate_key().decode()

f_key = Fernet(key)

class passwordM:
    def __init__(self):
        self.key = None
        self.file = None
       
    def create(self,path):
        # creates the key
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def find_key(self,path):
        with open(path, 'rb') as f:
            self.key = f.read()
        return self.key

    def encrypt_in_file(self, password: str, path) -> str:
        self.key = path
        f = Fernet(self.key)
        nw = f.encrypt(password.encode()).decode()
        return nw

    def decrypt_in_file(self,password: str, path) -> str:
        r_password = self.encrypt(password,path)
        
        nw = Fernet(self.key).decrypt(r_password.encode()).decode()
 
        return nw
    
    def encrypt(self, password: str) -> str:
        nw = f_key.encrypt(password.encode()).decode()
        return nw

    def decrypt(self, password: str) -> str:
        print(f"Decrypting {password}")
        decrypted = self.encrypt(password)
        print(f"Decrypted {decrypted}")
        dec = f_key.decrypt(decrypted).decode()
        print(f"Decrypted2 {dec}")
        return dec


# Global variables

directory = os.getcwd()
BASE_STRING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+?./<>\'\"[];:{}'

# Create encryption key

try:
    with open(file=directory + "\key.txt", mode='rb') as binary_file:
        KEY = binary_file.read()
except:
    with open(file=directory + "\key.txt", mode='wb') as binary_file:
        KEY = Fernet.generate_key()
        binary_file.write(KEY)

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
            password += BASE_STRING[random.randint(0, len(BASE_STRING) - 1)]
        i += 1
    return password

def encrypt(password: str) -> str:
    """
    Encrypts 'password' using our custom encryption algorithm.
    """
    f = Fernet(KEY)
    encoded = b64encode(f.encrypt(bytes(password, "utf-8"))).decode()
    return encoded

def decrypt(password: str) -> str:
    """
    Decrypts 'password' using our custom encryption algorithm.
    """
    f = Fernet(KEY)
    password = b64decode(password)
    password = f.decrypt(password).decode()
    return password

def hash(master_password: str) -> sha256:
    """
    Secures the master password.
    """
    return sha256(master_password.encode('utf-8')).hexdigest()

def verify(password: str) -> bool:
    """
    Checks if sha256('master_password') is the same as the locally stored master_password.
    """
    with open(file = directory + "\master_password.txt", mode='r') as f:
        master_password = f.read()
    return hash(password) == master_password