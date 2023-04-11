from cryptography.fernet import Fernet

# have to install the fernet import
#grabs csv file and turns it into a dictionary
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



    