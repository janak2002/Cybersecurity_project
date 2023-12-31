#import encryption libraries
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

#class that contains the functionality of the password manager
class PasswordManager:

    #initialization function
    def __init__(self):
        self.key = None
        self.password_file = None
        self.dict = {}
        self.mpassword=None

    #create master password
    def create_master_password(self):
        #takes user input and encrypts it into the master_password.bin file to store it
        self.mpassword=input('what would you like to be your master password: ')
        self.mpassword=self.mpassword.encode("utf-8")
        cipher = AES.new(self.key,AES.MODE_CBC)
        ciphered_data=cipher.encrypt(pad(self.mpassword,AES.block_size))

        with open ('master_password.bin','wb') as f:
            f.write(cipher.iv)
            f.write(ciphered_data)
        
            
    #fetches the already existing password from the password file and decrypts it
    def get_master_password(self):
        with open ('master_password.bin','rb') as f:
            iv=f.read(16)
            decrypt_data=f.read()

        cipher=AES.new(self.key,AES.MODE_CBC,iv=iv)
        self.mpassword=unpad(cipher.decrypt(decrypt_data),AES.block_size)
        return self.mpassword

    #generate encryption key and write it in the key file
    def generate_key(self,path):
        salt = b'\xa6\n\x14\xc8l\x124\xb2\xa6\xcd\xf1\x7f\x95 \xe9d\x7fN1H\\\xd8\r\xad\x1e\xfd\xbc\xaf\x85\xcf\xc28'
        self.mpassword='masterpassword'
        self.key=PBKDF2(self.mpassword,salt,32)
        with open (path, 'wb') as f:
            f.write(self.key)
        return self.key
    
    #encrypting some plain text (username, password, card name, card number, cvc, any credential with AES CBC mode)

    def encrypt_clear_text(self, clear_text,path):

        #make the cipher using a standard function new from the AES library
        cipher = AES.new(self.key,AES.MODE_CBC)

        #check that by chance the data you're encrypting isn't already 16,32, 48 bytes long
        if len(clear_text) % AES.block_size == 0:
            print('size of clear text is: ',len(clear_text))
            print("I don't get padded because I'm a size of the AES block!")
            padded_data = clear_text
        else:
            #if data isn't the size of a block then pad it until it is
            padded_data=pad(clear_text,AES.block_size)
            print('I get padded!')
        
        
        #just checking
        print('size of clear text is: ',len(clear_text))
       
        #encrypt your data
        ciphered_data=cipher.encrypt(padded_data)
        
        #write encrypted data into a binary file; first its iv (initialization vector), then the actual data, length of the encrypted
        #data will then be: 16 bytes (iv) + 16 bytes or 32 bytes or 48 bytes... of padded data
        with open (path,'ab') as f:
            f.write(cipher.iv)
            f.write(ciphered_data)

        
        #calculate the length of the encrypted data, later important for decrypting offset
        line_in_encryption_file=len(cipher.iv)+len(ciphered_data)
        print("A line in encryption file is: ", len(cipher.iv)+len(ciphered_data))
        return line_in_encryption_file
    
    #a function that checks if data was previously padded
    def is_padded(self,data):
        last_byte = data[-1]
        padding_length = last_byte

        # Check if the last 'padding_length' bytes are all equal to 'padding_length'
        return data[-padding_length:] == bytes([padding_length]) * padding_length
    
    #decryptor function
    def decrypt_cipher_text(self,path,line_lengths,list_of_site,a): 
        
        #which file contains your encrypted data = path
        self.password_file=path
       
        #at beginning offset is 0
        offset=0

        #into this list we shall store decrypted credentials
        cred_list=[]

        #just checking - size of encrypted file
        file_size = os.path.getsize('encrypted_text.bin')
        print(f"The size of {'encrypted_text.bin'} is {file_size} bytes.")
        
        #read from encrypted file
        with open(path, 'rb') as f:
            for i in range(len(line_lengths)):
               
                #positipon reading beginning at the byte offset
                f.seek(offset)
                print('this is offset: ',offset)
                #just checking
                print('here is your line length: ',line_lengths[i])
                #read iv and data
                iv=f.read(16)
                encrypted_data=f.read(line_lengths[i] - 16) 
                
                cipher=AES.new(self.key,AES.MODE_CBC,iv=iv)
                decrypted_data = cipher.decrypt(encrypted_data)

                #check if data was previously padded and unpad if so
                if not self.is_padded(decrypted_data):
                    print("I am not getting depadded")
                    unpadded_data = decrypted_data
                else:
                    print('unpadding...')
                    unpadded_data=unpad(decrypted_data,AES.block_size)
                
                #increase offset
                offset+=line_lengths[i]
                #add what you decripted to the list
                cred_list.append(unpadded_data)
                #checking                    
                print(cred_list)
                
        #make the result list that will contain the decrypted data divided into smaller arrays, login array size is 2
        #because there are two credentials
        if a=="logins":
            cred_list = cred_list[:len(cred_list)//2 * 2]
            result_list = [cred_list[i:i+2] for i in range(0, len(cred_list), 2)]

        #card array size is 4 because there are 4 credentials
        elif a=="cards":
            result_list=[cred_list[i:i+4] for i in range(0, len(cred_list), 4)]

        #card array size is 1 because there is only one content
        elif a=="secures":
            result_list=cred_list
                        
        #create self.dict
        #Logins: keys are the sites and values are credentials for logins
        #Cards: keys are the card names and values are credentials of the card
        #Secure notes: keys are the secure notes names and values are contents of the note
        for i in range(len(list_of_site)):
                self.dict[list_of_site[i]] = result_list[i]
               
        return self.dict
    
#clear file
def clear_file(file_path):
        with open(file_path, 'w'):  # 'wb' for binary files
            pass                


## a main fucntion which is not incorporated in the project and was used to test the encryption by providing some mock up
##dictionary of logins
# def main():
#     clear_file('encrypted_text.bin')
#     pw=PasswordManager()
    
#     key=pw.generate_key('myfunkey.key')
#     print(key)
#     passi=pw.get_master_password()
#     print(passi)
#     #list_of_logins=[]  #contains site,username,password for all your logins
#     list_of_credentials=[]
#     line_lengths=[]
#     list_of_site=[]
    
    
#     dictionary={b'yt':[b'jana_1',b'ivana123'],
#                 b'instagram':[b'jana_k',b'bassamcool'],
#                 b'utwente':[b'j.klaric@student.utwente',b'janaaaaa23']               
#                 }
   
#     for site,credentials in dictionary.items():
#         #create list of sites and list of credentials
#         list_of_site.append(site)
#         list_of_credentials.extend(credentials)

#     #encrypt your data and make line_lengths list
#     for i in range (len(list_of_credentials)):
#         print('encrypting: ',list_of_credentials[i])
#         line_lengths.append(pw.encrypt_clear_text(list_of_credentials[i],'encrypted_text.bin'))
        
   
#     print(line_lengths)
    
#     #decrypt your data
#     decrypted_credentials=pw.decrypt_cipher_text('encrypted_text.bin',line_lengths,list_of_site)
#     print(decrypted_credentials)

   

# if __name__ == "__main__":
#     main()
