from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.dict = {}
        self.mpassword=None

   
    def create_master_password(self):
        self.mpassword=input('what would you like to be your master password')
        with open ('master_password.bin','w') as f:
            f.write(self.mpassword)

    def get_master_password(self):
        with open ('master_passwordi.bin','r') as f:
            self.mpassword=f.read()
        return self.mpassword

    def generate_key(self,path):
        salt = b'\xa6\n\x14\xc8l\x124\xb2\xa6\xcd\xf1\x7f\x95 \xe9d\x7fN1H\\\xd8\r\xad\x1e\xfd\xbc\xaf\x85\xcf\xc28'
        self.mpassword='masterpassword'
        self.key=PBKDF2(self.mpassword,salt,32)
        return self.key

    def encrypt_clear_text(self, clear_text,path):

        cipher = AES.new(self.key,AES.MODE_CBC)
        if len(clear_text) % AES.block_size == 0:
            print('size of clear text is: ',len(clear_text))
            print("I don't get padded because I'm a size of the AES block!")
            padded_data = clear_text
            
        else:
            padded_data = pad(clear_text, AES.block_size)
            print('size of clear text is: ',len(clear_text))
            print('I get padded!')

        ciphered_data = cipher.encrypt(padded_data)
        #print('size of long data is: ',len(ciphered_data))
        #ciphered_data=cipher.encrypt(pad(clear_text,AES.block_size))

        with open (path,'ab') as f:
            f.write(cipher.iv)
            f.write(ciphered_data)

        
        #print("Ciphered Data:", ciphered_data)
        line_in_encryption_file=len(cipher.iv)+len(ciphered_data)
        print("A line in encryption file is: ", len(cipher.iv)+len(ciphered_data))
        return line_in_encryption_file

    

    def decrypt_cipher_text(self,path,list_of_logins,file_length,line_lengths): 
        line_size = 32
        line_number = 0
        self.password_file=path
        increment=0

        file_size = os.path.getsize('encrypted_text.bin')
        print(f"The size of {'encrypted_text.bin'} is {file_size} bytes.")
        with open(path, 'rb') as f:
            for i in range(file_length):
                cred_list=[]
                
                for j in range(2):
                    print('increment is: ',increment)
                    offset = (line_number+increment)*line_size
                    f.seek(offset)
                    print('ovo je offset: ',offset)
                    iv=f.read(16)
                    print('ovo je length: ',len(iv))
                    encrypted_data=f.read(line_size - 16) 
                    print('encrypted data is: ',encrypted_data)
                    cipher=AES.new(self.key,AES.MODE_CBC,iv=iv)
                    print('size of block: ',AES.block_size)
                    #decrypted_data=unpad(cipher.decrypt(encrypted_data),AES.block_size)
                    decrypted_data=cipher.decrypt(encrypted_data),AES.block_size
                    print('size of decrypted data', len(decrypted_data))

                    if len(decrypted_data) // AES.block_size < 1:
                        print('breeeeeeee')
                        decrypted_data = unpad(decrypted_data, AES.block_size)
                    else:
                        print('breeee 2')
                        
                    #ecoded_data = [item.decode('utf-8') for item in decrypted_data]
                    cred_list.append(decrypted_data)
                    increment+=1                   
                increment-=1
                
                print(cred_list)
                self.dict[list_of_logins[line_number * 3]]=cred_list   
                line_number+=1
               
        return self.dict
    
    
def clear_file(file_path):
        with open(file_path, 'w'):  # 'wb' for binary files
            pass                

def main():
    clear_file('encrypted_text.bin')
    pw=PasswordManager()
    #pw.create_master_password()
    key=pw.generate_key('myfunkey.key')
    print(key)
    passi=pw.get_master_password()
    print(passi)
    list_of_logins=[]  #contains site,username,password for all your logins
    list_of_credentials=[]
    line_lengths=[]
    
    
    dictionary={b'yt':[b'jana_1',b'ivana123'],
                b'instagram':[b'jana_k',b'bassamcool'],
                b'utwente':[b'j.klaric@student.utwente',b'janaaaaa23']               
                }
   
    for site,credentials in dictionary.items():
        list_of_logins.append(site)
        list_of_logins.extend(credentials)
        list_of_credentials.extend(credentials)

    for i in range (len(list_of_credentials)):
        print('encrypting: ',list_of_credentials[i])
        line_lengths.append(pw.encrypt_clear_text(list_of_credentials[i],'encrypted_text.bin'))
        
   
    print(line_lengths)
    print(list_of_logins)
    dict_2=pw.decrypt_cipher_text('encrypted_text.bin',list_of_logins,len(dictionary),line_lengths)
    print(dict_2)
    file_path = 'encrypted_text.bin'  # Replace with the actual path to your .bin file

    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        print(f"The size of {file_path} is {file_size} bytes.")
   

if __name__ == "__main__":
    main()
