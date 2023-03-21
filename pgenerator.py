import random
from hashlib import sha256

def create_random_password() -> str:
    """
    Creates a random password which uses a total of 15 characters with dashes (-) between 5.
    """
    #TODO
    pass

def encrypt(password: str) -> str:
    """
    Encrypts 'password' using our custom encryption algorithm.
    """
    #TODO
    pass

def decrypt(password: str) -> str:
    """
    Decrypts 'password' using our custom encryption algorithm.
    """
    #TODO
    pass

def hash(master_password: str) -> sha256:
    """
    Secures the master password.
    """
    #TODO
    pass

def verify(master_password: str) -> bool:
    """
    Checks if sha256('master_password') is the same as the locally stored master_password.
    """
    #TODO
    pass
