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

directory = os.getcwd()
BASE_STRING = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+?./<>\'\"[];:{}'

encryption_dict = {}
for i in range(len(BASE_STRING) - 1):
    encryption_dict[BASE_STRING[i]] = BASE_STRING[i + 1]
    encryption_dict['-'] = '-'
    encryption_dict[':'] = ':'

decryption_dict = {}
for i in range(len(BASE_STRING) - 1):
    decryption_dict[BASE_STRING[i + 1]] = BASE_STRING[i]
    decryption_dict['-'] = '-'
    decryption_dict[':'] = ':'
    decryption_dict['a'] = 'a'

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
    encrypted_string = ''
    for char in password:
        encrypted_string += encryption_dict[char]
    return encrypted_string

def decrypt(password: str) -> str:
    """
    Decrypts 'password' using our custom encryption algorithm.
    """
    decrypted_string = ''
    for char in password:
        decrypted_string += decryption_dict[char]
    return decrypted_string

def hash(master_password: str) -> sha256:
    """
    Secures the master password.
    """
    return sha256(master_password.encode('utf-8')).hexdigest()

def verify(password: str) -> bool:
    """
    Checks if sha256('master_password') is the same as the locally stored master_password.
    """
    with open(file = directory + "\data\master_password.txt", mode='r') as f:
        master_password = f.read()
    return hash(password) == master_password