from AES_final_encryption import PasswordManager
import os

#WHAT I STILL WANNA DO
#add clues for password




#clear file
def clear_file(file_path):
        with open(file_path, 'w'):  # 'wb' for binary files
            pass   


def master_password_set(path, pw):
     is_file_empty=os.path.getsize(path) == 0
     if is_file_empty:
          pw.create_master_password()
          print('Password set!')
          return 0
     else:
          print('I read your master password to be: ')
          print(pw.get_master_password())
          return pw.get_master_password()

def check_master_password(user_input,actual_password):
     if user_input==actual_password:
          return True
     else:
          #print("Seems like you've forgotten your password, here's your clue: ",clue)
          return False
     
def main():
    clear_file('encrypted_text.bin')
    pw=PasswordManager()
    
    key=pw.generate_key('myfunkey.key')
    print(key)
    passi=pw.get_master_password()
    print(passi)
    list_of_credentials=[]
    line_lengths=[]
    list_of_site=[]
    
    
    dictionary={b'yt':[b'jana_1',b'ivana123'],
                b'instagram':[b'jana_k',b'bassamcool'],
                b'utwente':[b'j.klaric@student.utwente',b'janaaaaa23']               
                }
   
    for site,credentials in dictionary.items():
        #create list of sites and list of credentials
        list_of_site.append(site)
        list_of_credentials.extend(credentials)

    #encrypt your data and make line_lengths list
    for i in range (len(list_of_credentials)):
        print('encrypting: ',list_of_credentials[i])
        line_lengths.append(pw.encrypt_clear_text(list_of_credentials[i],'encrypted_text.bin'))
        
   
    print(line_lengths)
    
    #decrypt your data
    decrypted_credentials=pw.decrypt_cipher_text('encrypted_text.bin',line_lengths,list_of_site)
    print(decrypted_credentials)

    #unlock the app with masterpassword
    mp=master_password_set('master_password.bin',pw)
    unlock=input('Enter master password please: ')
    print(check_master_password(unlock,mp))

   

if __name__ == "__main__":
    main()
