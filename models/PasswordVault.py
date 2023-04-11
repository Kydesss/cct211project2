import csv
from models.base import Model
from utils.passwordEncrypt import passwordM 
import utils as ut

pm = passwordM()
class PasswordVault(Model):
    table_name = "passwords"

    def __init__(self, id:int=None, username:str=None, password:str=None, url:str=None):
        self.id = id
        self.username = username
        self.password = password
        self.url = url

    @classmethod
    def create_table(cls):
        print("Creating passwords table..")
        query = f"""CREATE TABLE IF NOT EXISTS {cls.table_name} 
                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                url TEXT NOT NULL
            )"""
        print(query)
        cls._execute_query(query)

    @classmethod
    def get_passwords(cls):
        """Returns all passwords with username instead of user_id"""
        query = f"""SELECT passwords.id, passwords.url, passwords.username, passwords.password
                FROM passwords
                ORDER BY passwords.id DESC
                """
        result = cls._execute_query(query)
        return result
    
    @classmethod
    def add_password(cls, username, password, url):
        """Adds a password to the database"""
        encrypted_password = ut.encrypt(password)
        query = f"""INSERT INTO passwords ( username, password, url)
            VALUES ( '{username}', '{encrypted_password}', '{url}')"""
        cls._execute_query(query)
        return cls(username=username, password=encrypted_password, url=url)
    
    
    @classmethod
    def delete_password(self):
        """Deletes a password from the database"""
        query = f"""DELETE FROM passwords WHERE id = {self.id}"""
        self._execute_query(query)
        

    

    @classmethod
    def import_passwords(cls, passwords: csv):
        """
        Imports CSV password files from Chrome or Edge.
        """
        csv_reader = csv.reader(passwords)

        for row in csv_reader:
            username = row[0]
            password = ut.encrypt(row[3])
            url = row[2]
            cls.add_password(username, password, url)

    @classmethod
    def export_passwords(cls, dir_name: str):
        """
        Exports CSV password files from Chrome or Edge.
        """
        passwords = cls.get_passwords()
        export = [['name', 'url', 'username', 'password']]
        for password in passwords:
            
            export.append([password[1], password[1], password[2], ut.decrypt(password[3])])
            
        with open(file=dir_name, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(export)
            
        

