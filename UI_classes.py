#import libraries and functions from other files
import flet as ft
from AES_finalenc_masterenc import clear_file
from AES_finalenc_masterenc import PasswordManager
from password_generator import generate_password
import os
import json
from flet import (
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    Page,
    Row,
    TextField,
    UserControl,
    colors,
    icons,
)
#class of Task - a task is a set of site name, login and password
class Task(ft.UserControl):
    #initialization function - attributes if class defined
    def __init__(self, task_name_site,task_name_username, task_name_password,dictionary_of_logins,list_of_sites,list_of_creds,line_lengths,task_delete):
        super().__init__()
        self.task_name_site = task_name_site
        self.task_name_username = task_name_username
        self.task_name_password = task_name_password
        self.dictionary_of_logins=dictionary_of_logins
        self.list_of_site=list_of_sites
        self.list_of_credentials=list_of_creds
        self.line_lengths=line_lengths
        self.task_delete = task_delete
        
    #update function - runs every time you call update
    def build(self):
        
        self.tasks = ft.Column()
        
       
        #define the display view - how the tasks will look normally
        self.display_task_site = ft.Text(value=self.task_name_site,size=25)
        self.display_task_username = ft.Text(value=self.task_name_username,size=25)
        self.display_task_password = ft.Text(value=self.task_name_password,size=25)

        
        #define edit view - how a screen will look when you press edit button
        self.edit_name_site = ft.TextField(label="site")
        self.edit_name_username = ft.TextField(label="username")
        self.edit_name_password = ft.TextField(label="password")

        #put the display elements on the screen 
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Row(
                    spacing=40,
                    controls=[
                        self.display_task_site,
                        ft.Text(value=""),
                        self.display_task_username,
                        ft.Text(value=""),
                        self.display_task_password,
                        ft.Text(value=""),
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
        #put the edit elements on the screen
        self.edit_view = ft.Row(
            visible=False,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[ft.Row(
                spacing=5,
                controls=[
                    
                        self.edit_name_site,
                        self.edit_name_username,
                        self.edit_name_password,
                        ft.IconButton(
                        icon=ft.icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.colors.GREEN,
                        tooltip="Update To-Do",
                        on_click=self.save_clicked,
                    )
                    
    	            
                ])   
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    #what happens when you click edit 
    def edit_clicked(self, e):
        self.edit_name_site.value = self.display_task_site.value
        self.edit_name_username.value = self.display_task_username.value
        self.edit_name_password.value = self.display_task_password.value
        #switch views
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()
    #what happens when you click save
    def save_clicked(self, e):
        
        pw=PasswordManager()
        self.line_lengths=[]

        self.key=pw.generate_key('myfunkey.key')
        #set the display values to what you just entered
        self.display_task_site.value = self.edit_name_site.value
        self.display_task_username.value = self.edit_name_username.value
        self.display_task_password.value = self.edit_name_password.value
        #add the task to the dictionary of logins
        self.dictionary_of_logins[self.display_task_site.value]=[self.display_task_username.value.encode("utf-8"),self.display_task_password.value.encode("utf-8")]
        
        #clear files containing info for decrypting
        clear_file("encrypted_text.bin")
        clear_file("info.txt")
        #place the site names and credentials in lists while going through the dictionary that stores tasks
        for site,credentials in self.dictionary_of_logins.items():
            #create list of sites and list of credentials
            if site not in self.list_of_site:
                self.list_of_site.append(site)
                self.list_of_credentials.extend(credentials)

        #encrypt the credentials and add the length of the encrypted data to the list line_lengths    
        for i in range (len(self.list_of_credentials)):

            print('encrypting: ',self.list_of_credentials[i])
            self.line_lengths.append(pw.encrypt_clear_text(self.list_of_credentials[i],'encrypted_text.bin'))
        
        
    
        #go back to the display view
        self.display_view.visible = True
        self.edit_view.visible = False
        #printing for checking
        print(self.dictionary_of_logins)
        print(self.list_of_site)
        print(self.list_of_credentials)
        print(self.line_lengths)
        #in info.txt write line lengths in the first row and site names to which you want to store the logins in the second row
        with open ("info.txt","w") as f:
            for i in range(len(self.line_lengths)):
                f.write(str(self.line_lengths[i])+" ")
            f.write('\n')
            for i in range(len(self.list_of_site)):
                f.write(self.list_of_site[i]+" ")

        
        self.update()
       

    #what happens when you click delete
    def delete_clicked(self, e):
        self.task_delete(self)
        
#Logins class
class Logins(UserControl):
    #initialization function, define attributes
    def __init__(self,dictionary_of_logins,list_of_sites,list_of_creds,line_lengths):
        super().__init__()
        self.dictionary_of_logins=dictionary_of_logins
        self.list_of_site=list_of_sites
        self.list_of_credentials=list_of_creds
        self.line_lengths=line_lengths

    def build(self):
   
        #make a password manager
        pw=PasswordManager()
        #what you first see on your Logins screen
        self.new_task = ft.Text(value="Welcome to your logins",size=50,text_align="LEFT")
        self.stored_tasks=ft.Column()
        self.tasks=ft.Column()
        #read the key which was used for encryption
        with open ("myfunkey.key","rb") as f:
            pw.key=f.read()
        #check if there is encrypted data
        if os.path.getsize("encrypted_text.bin") !=0:
            #if there is ancrypted data, check if you have line legths stored
            with open("info.txt", 'r') as file:
                # Check if the file is empty by attempting to read the first character
                first_char = file.read(1)
                a= not first_char
                if a:
                    print("info_file_empty")
                else:
                    #if you have all of these info, read them out
                    with open ("info.txt","r") as f:
                        #read line lengths in bits
                        data=f.readline()
                        list_of_numbers = data.split()
                        self.line_lengths = [int(num) for num in list_of_numbers]
                        #read site names
                        data_2=f.readline()
                        self.list_of_site=data_2.split()
                    #decrypt stored logins
                    stored_logins=pw.decrypt_cipher_text("encrypted_text.bin",self.line_lengths,self.list_of_site,"logins")
                    print("SOME PASSWORDS STORED",stored_logins)
                #create tasks of the stored logins 
                for key,values in stored_logins.items():
                    decoded_values = [value.decode('utf-8') for value in values]
                    task=Task(key,decoded_values[0],decoded_values[1],self.dictionary_of_logins,self.list_of_site,self.list_of_credentials,self.line_lengths, self.task_delete)
                    #add them to the screen controls
                    self.stored_tasks.controls.append(task)
                    self.tasks.controls.append(task)
                #add the already existing credentials to the list of credenatials 
                self.dictionary_of_logins=stored_logins
                for site,credentials in self.dictionary_of_logins.items():
                    #create list of credentials
                    self.list_of_credentials.extend(credentials)
                
        print('update list site: ',self.list_of_site)
        print('update list of cred: ', self.list_of_credentials)
        self.tasks = Column()

        #put the stored tasks on the screen as well as the new tasks a person makes
        return Column(
            width=1000,
            alignment="SPACE_BETWEEN",
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        ft.Text(value=""),
                        ft.IconButton(
                                        icon=ft.icons.ADD,
                                        tooltip="Add password",
                                        on_click=self.add_clicked,
                                    )
                    ]
                ),
                self.stored_tasks,
                self.tasks,
            ],
        )
    #what happens when you click add
    def add_clicked(self, e):
        #create a new task for the user to fill out
        task = Task("site","username","password",self.dictionary_of_logins,self.list_of_site,self.list_of_credentials,self.line_lengths, self.task_delete)
        
        
        self.tasks.controls.append(task)
        
       
        self.update()
        
    #what happens when you press delete
    def task_delete(self, task):
        if task in self.tasks.controls:
            self.tasks.controls.remove(task)
        elif task in self.stored_tasks.controls:
            self.stored_tasks.controls.remove(task)
        #remove the task from the dictionary, cred list, site list
        self.dictionary_of_logins.pop(task.task_name_site,None)
        self.list_of_site.remove(task.task_name_site)
        self.list_of_credentials.remove(task.task_name_username.encode('utf-8'))
        self.list_of_credentials.remove(task.task_name_password.encode('utf-8'))

        #print checking 
        print('novi rjecnik',self.dictionary_of_logins)
        print('nova login lista',self.list_of_site)
        print('nova cred lista',self.list_of_credentials)
        self.update()


#Cardtask class
class CardTask(UserControl):
    #define attributes with the initialization function
    def __init__(self,card_name,card_holder,card_number,exp_date,CVC,dictionary_of_cards,list_of_names,list_of_creds,line_lengths,task_delete):
        super().__init__()
        self.card_name=card_name
        self.card_holder=card_holder
        self.card_number=card_number
        self.exp_date=exp_date
        self.cvc=CVC
        self.dictionary_of_cards=dictionary_of_cards
        self.list_of_names=list_of_names
        self.list_of_credentials=list_of_creds
        self.line_lengths=line_lengths
        self.task_delete = task_delete

    def build(self):
        
        self.tasks=ft.Column()
        #make the display view
        self.display_task_card_name = ft.Text(value=self.card_name,size=27)
        self.display_task_card_holder = ft.Text(value=self.card_holder,size=20)
        self.display_task_card_number = ft.Text(value=self.card_number,size=20)
        self.display_task_exp_date = ft.Text(value=self.exp_date,size=20)
        self.display_task_cvc = ft.Text(value=self.cvc,size=20)

        #make the edit view
        self.edit_name_card_name = ft.TextField(label="card name",text_size=10)
        self.edit_name_card_holder = ft.TextField(label="card holder",text_size=10)
        self.edit_name_card_number = ft.TextField(label="card number",text_size=10)
        self.edit_name_exp_date= ft.TextField(label="exp date",text_size=10)
        self.edit_name_cvc= ft.TextField(label="CVC",text_size=10)

        #put the display view on screen
        self.display_view = ft. Card(
            content=ft.Container(
                content=
            ft.Column(
            
            alignment="SPACE_BETWEEN",
            spacing=10,
            controls=[  ft.Row([
                              ft.Text(value=""),
                             self.display_task_card_name,
                        ]),
                     
                      ft.Row([
                        ft.Text(value=""),
                        self.display_task_card_holder,
                      ]),
                      ft.Row([
                          ft.Text(value=""),
                        self.display_task_card_number,
                      ]),
                        
                      
                        ft.Text(value=""),
                        ft.Row(spacing = 5,
                            controls=[
                        ft.Text(value=""),
                        self.display_task_exp_date,
                        ft.Text(value=""),
                        self.display_task_cvc,
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete",
                            on_click=self.delete_clicked,
                        )
                        ]
                        )
                    
                
            ],
        ),
        width=660,
        height=250,
        padding=5
        )
        
        )
        #put the edit view on the screen 
        self.edit_view = ft.Card(
            visible=False,
            
            content=ft.Column(
                alignment="SPACE_BETWEEN",
                spacing=10,
                controls=[
                        self.edit_name_card_name,
                        self.edit_name_card_holder,
                        self.edit_name_card_number,
                        ft.Row([
                            self.edit_name_exp_date,
                            self.edit_name_cvc,
                            ft.IconButton(
                            icon=ft.icons.DONE_OUTLINE_OUTLINED,
                            icon_color=ft.colors.GREEN,
                            tooltip="Update To-Do",
                            on_click=self.save_clicked,
                            )
                        ])
       
                ]),
                width=660,
                height=250
                 
            
        )
        return ft.Column(controls=[self.display_view, self.edit_view])
    #when edit is clicked change modes from display to edit
    def edit_clicked(self, e):
        self.edit_name_card_name.value = self.display_task_card_name.value
        self.edit_name_card_holder.value = self.display_task_card_holder.value
        self.edit_name_card_number.value = self.display_task_card_number.value
        self.edit_name_exp_date.value = self.display_task_exp_date.value
        self.edit_name_cvc.value = self.display_task_cvc.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    #what happens when you click save
    def save_clicked(self, e):
        print("save clicked")
        pw=PasswordManager()
        self.line_lengths=[]

        #change the display view to what the user put in
        self.key=pw.generate_key('myfunkey.key')
        self.display_task_card_name.value = self.edit_name_card_name.value
        self.display_task_card_holder.value = self.edit_name_card_holder.value
        self.display_task_card_number.value = self.edit_name_card_number.value
        self.display_task_exp_date.value = self.edit_name_exp_date.value
        self.display_task_cvc.value = self.edit_name_cvc.value
        #put the card in the card dictionary
        self.dictionary_of_cards[self.display_task_card_name.value]=[self.display_task_card_holder.value.encode("utf-8"),self.display_task_card_number.value.encode("utf-8"),self.display_task_exp_date.value.encode("utf-8"),self.display_task_cvc.value.encode("utf-8")]
        
        #clear info file and the encrypted file
        clear_file("encrypted_cards.bin")
        clear_file("info_cards.txt")
        #scan through the dictionary of cards and divide them into the card name and the credentials that have to be encrypted
        for name,credentials in self.dictionary_of_cards.items():
            #create list of sites and list of credentials
            if name not in self.list_of_names:
                self.list_of_names.append(name)
                self.list_of_credentials.extend(credentials)
        #encrypt credentials      
        for i in range (len(self.list_of_credentials)):

            print('encrypting: ',self.list_of_credentials[i])
            self.line_lengths.append(pw.encrypt_clear_text(self.list_of_credentials[i],'encrypted_cards.bin'))
        
        
        #change modes from edit to display

        self.display_view.visible = True
        self.edit_view.visible = False
        #print check
        print(self.dictionary_of_cards)
        print(self.list_of_names)
        print(self.list_of_credentials)
        print(self.line_lengths)
        #write into the info file the lengths of pieces of data that are encrypted
        with open ("info_cards.txt","w") as f:
            for i in range(len(self.line_lengths)):
                f.write(str(self.line_lengths[i])+" ")
            f.write('\n')
            #write the names of the cards in the info file - these don't have to be encrypted
            for i in range(len(self.list_of_names)):
                f.write(self.list_of_names[i]+"\n")

        
        self.update()
    #delete function
    def delete_clicked(self, e):
        self.task_delete(self)
#Card class
class Card(UserControl):
    #initialize the function
    def __init__(self,dictionary_of_cards,list_of_names,list_of_creds,line_lengths):
        super().__init__()
        self.dictionary_of_cards=dictionary_of_cards
        self.list_of_names=list_of_names
        self.list_of_credentials=list_of_creds
        self.line_lengths=line_lengths
       

    def build(self):
   

        pw=PasswordManager()
        #first thing that will be displayed on the screen when the user clicks on cards
        self.new_task = ft.Text(value="Welcome to your Cards",size=50,text_align="LEFT")
        self.stored_tasks=ft.Column()
        self.tasks=ft.Column()
        #get the key from the myfunkey.key file for decrypting
        with open ("myfunkey.key","rb") as f:
            pw.key=f.read()
        #check if encrypted data exists
        if os.path.getsize("encrypted_cards.bin") !=0:
            #check if the info  file is not empty - should be filled with info if encrypted data existed
            with open("info_cards.txt", 'r') as file:
              
                first_char = file.read(1)
                a= not first_char
                if a:
                    print("infocard_file_empty")
                else:

                    with open ("info_cards.txt","r") as f:
                        #get the line lengths from the file
                        data=f.readline()
                        list_of_numbers = data.split()
                        self.line_lengths = [int(num) for num in list_of_numbers]

                        #get names of cards
                        self.list_of_names=f.readlines()
                        self.list_of_names = [name.strip() for name in self.list_of_names]
                    
                        print("this is the list of names",self.list_of_names)
                        
                    #decrypted the data that's already stored in the encrypted files
                    stored_cards=pw.decrypt_cipher_text("encrypted_cards.bin",self.line_lengths,self.list_of_names,"cards")
                    print("SOME CARDS STORED",stored_cards)
                    #make tasks out of stored data and put it on the screen
                    for key,values in stored_cards.items():
                        decoded_values = [value.decode('utf-8') for value in values]
                        task=CardTask(key,decoded_values[0],decoded_values[1],decoded_values[2],decoded_values[3],self.dictionary_of_cards,self.list_of_names,self.list_of_credentials,self.line_lengths, self.task_delete)
                        self.stored_tasks.controls.append(task)
                        self.tasks.controls.append(task)
                       
                    self.dictionary_of_cards=stored_cards
                    for name,credentials in self.dictionary_of_cards.items():
                        #create list of sites and list of credentials
                        self.list_of_credentials.extend(credentials)
        #updated lists prints       
        print('update list site: ',self.list_of_names)
        print('update list of cred: ', self.list_of_credentials)
        self.tasks = Column()

        # application's root control (i.e. "view") containing all other controls
        return Column(
            width=2000,
            alignment="SPACE_BETWEEN",
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        ft.Text(value=""),
                        ft.IconButton(
                                        icon=ft.icons.ADD,
                                        tooltip="Add password",
                                        on_click=self.add_clicked,
                                    )
                    ]
                ),
                self.stored_tasks,
                self.tasks,
            ],
        )
    #when add is clicked make a new task and append it to the controls (put it on the screen)
    def add_clicked(self, e):
        task = CardTask("name","holder","number","expdate","cvc",self.dictionary_of_cards,self.list_of_names,self.list_of_credentials,self.line_lengths, self.task_delete)
        
        
        self.tasks.controls.append(task)
        
       
        self.update()
    #delete task - remove the credentials from the list of credentials and the card from dictionary
    def task_delete(self, task):
        if task in self.tasks.controls:
            self.tasks.controls.remove(task)
        elif task in self.stored_tasks.controls:
            self.stored_tasks.controls.remove(task)
        self.dictionary_of_cards.pop(task.card_name,None)
        self.list_of_names.remove(task.card_name)
        self.list_of_credentials.remove(task.card_holder.encode('utf-8'))
        self.list_of_credentials.remove(task.card_number.encode('utf-8'))
        self.list_of_credentials.remove(task.exp_date.encode('utf-8'))
        self.list_of_credentials.remove(task.cvc.encode('utf-8'))

        #print check
        print('novi rjecnik karte',self.dictionary_of_cards)
        print('nova login lista karte',self.list_of_names)
        print('nova cred lista karte',self.list_of_credentials)
        self.update()

#secure notes task class
class SecureTask(UserControl):
    #initialize
    def __init__(self,task_name, task_content,dictionary_of_secures,list_of_snames,list_of_creds,line_lengths,task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_content = task_content
        
        self.dictionary_of_secures=dictionary_of_secures
        self.list_of_snames=list_of_snames
        self.list_of_credentials=list_of_creds

        self.line_lengths=line_lengths
        self.task_delete = task_delete
        
    def build(self):
        self.tasks = ft.Column()
        
       
        
        self.display_task_name = ft.Text(value=self.task_name,size=25)
        self.display_task_content = ft.Text(value=self.task_content,size=15)
 
        self.edit_task_name = ft.TextField(label="Name")
        self.edit_task_content = ft.TextField(label="Content")

        #display view definition
        self.display_view = ft.Column(
            spacing=10,
            controls=[  
                        self.display_task_name,
                        ft.Text(value=""),
                        self.display_task_content,
                        ft.Text(value=""),
                        ft.Row([
                            ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        )
                        ])
                        
                    ]
        )
        #edit view definition 
        self.edit_view = ft.Column(
                visible=False,
                spacing=10,
                controls=[
                    
                        self.edit_task_name,
                        self.edit_task_content,
                        ft.IconButton(
                        icon=ft.icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.colors.GREEN,
                        tooltip="Update",
                        on_click=self.save_clicked,
                    )
                    
    	            
        ]) 
        #put the display view on screen
        return ft.Column(controls=[self.display_view, self.edit_view])
    #edit clicked - change modes from display to edit
    def edit_clicked(self, e):
        self.edit_task_name.value = self.display_task_name.value
        self.edit_task_content.value = self.display_task_content.value
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    
    def save_clicked(self, e):
        print("save clicked")
        pw=PasswordManager()
        self.line_lengths=[]

        self.key=pw.generate_key('myfunkey.key')
        #change the display view and add the secure note information into the dictionary of secures
        self.display_task_name.value = self.edit_task_name.value
        self.display_task_content.value = self.edit_task_content.value
        self.dictionary_of_secures[self.display_task_name.value]=[self.display_task_content.value.encode("utf-8")]
        
        #clear files of information and encryption
        clear_file("encrypted_secures.bin")
        clear_file("info_secure.txt")
        #append the name of the secure note and the content of it into the credentials list
        for site,credentials in self.dictionary_of_secures.items():
            #create list of sites and list of credentials
            if site not in self.list_of_snames:
                self.list_of_snames.append(site)
                self.list_of_credentials.extend(credentials)
        print('secures list of credentials', self.list_of_credentials)

        #encrypt all the information in the secures dictioanary 
        for i in range (len(self.list_of_credentials)):

            print('encrypting: ',self.list_of_credentials[i])
            self.line_lengths.append(pw.encrypt_clear_text(self.list_of_credentials[i],'encrypted_secures.bin'))
        
        
        
        #change modes from edit to display
        self.display_view.visible = True
        self.edit_view.visible = False
        print(self.dictionary_of_secures)
        print(self.list_of_snames)
        print(self.list_of_credentials)
        print(self.line_lengths)
        #write the lengths of encrypted credentials into the info file as well as the names of the secure notes
        with open ("info_secure.txt","w") as f:
            for i in range(len(self.line_lengths)):
                f.write(str(self.line_lengths[i])+" ")
            f.write('\n')
            for i in range(len(self.list_of_snames)):
                f.write(self.list_of_snames[i]+" ")

        
        self.update()
    #delete
    def delete_clicked(self, e):
        self.task_delete(self)

class Secure(UserControl):
    #initialize
    def __init__(self,dictionary_of_secures,list_of_snames,list_of_creds,line_lengths):
        super().__init__()
        self.dictionary_of_secures=dictionary_of_secures
        self.list_of_snames=list_of_snames
        self.list_of_credentials=list_of_creds
        self.line_lengths=line_lengths
        
    def build(self):
        pw=PasswordManager()
        #first thing that is written on the screen when the user clickes on the secure notes
        self.new_task = ft.Text(value="Welcome to your secure notes",size=50,text_align="LEFT")
        self.stored_tasks=ft.Column()
        self.tasks=ft.Column()
        #read the key for the decryption
        with open ("myfunkey.key","rb") as f:
            pw.key=f.read()
        #check if there already is encrypted data
        if os.path.getsize("encrypted_secures.bin") !=0:

            with open("info_secure.txt", 'r') as file:
                # Check if the file is empty by attempting to read the first character
                first_char = file.read(1)
                a= not first_char
                if a:
                    print("info_file_empty")
                else:
                    #if there is already data
                    with open ("info_secure.txt","r") as f:
                        #read out the lengths of data that you have to decrypt
                        data=f.readline()
                        list_of_numbers = data.split()
                        self.line_lengths = [int(num) for num in list_of_numbers]
                        #read the names of the secure notes
                        self.list_of_snames=f.readlines()
                        self.list_of_snames = [name.strip() for name in self.list_of_snames]
                        print("this is the list of snames",self.list_of_snames)
                    #decrypt the already existing and saved secure notes
                    stored_secures=pw.decrypt_cipher_text("encrypted_secures.bin",self.line_lengths,self.list_of_snames,"secures")
                    print("SOME SECURE NOTES STORED",stored_secures)
                #append the already existing secure notes to the controls of what's on the screen
                for key,value in stored_secures.items():
                    decoded_value = value.decode('utf-8')
                    task=SecureTask(key,decoded_value,self.dictionary_of_secures,self.list_of_snames,self.list_of_credentials,self.line_lengths, self.task_delete)
                    self.stored_tasks.controls.append(task)
                    self.tasks.controls.append(task)
                    

                self.dictionary_of_secures=stored_secures
                for site,credentials in self.dictionary_of_secures.items():
                    #create lis of contents/credentials
                    self.list_of_credentials.append(credentials)
        #print check
        print('update list snames: ',self.list_of_snames)
        print('update list of cred: ', self.list_of_credentials)
        self.tasks = Column()
    
         # application's root control (i.e. "view") containing all other controls
        return Column(
            width=1000,
            alignment="SPACE_BETWEEN",
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        ft.Text(value=""),
                        ft.IconButton(
                                        icon=ft.icons.ADD,
                                        tooltip="Add secure note",
                                        on_click=self.add_clicked,
                                    )
                    ]
                ),
                self.stored_tasks,
                self.tasks,
            ],
        )
    #when add is clicked - add a new task of type Secure and append it to the screen control
    def add_clicked(self, e):
        task = SecureTask("name","content",self.dictionary_of_secures,self.list_of_snames,self.list_of_credentials,self.line_lengths, self.task_delete)
        
        
        self.tasks.controls.append(task)
        
       
        self.update()
    #delete the secure note
    def task_delete(self, task):

        if task in self.tasks.controls:
            self.tasks.controls.remove(task)
        elif task in self.stored_tasks.controls:
            self.stored_tasks.controls.remove(task)
        #remove the task from the dictionary, the name from snames list and the content from the credentials lsit
        self.dictionary_of_secures.pop(task.task_name,None)
        self.list_of_snames.remove(task.task_name)
        self.list_of_credentials.remove(task.task_content.encode('utf-8'))
        
       
        print('novi rjecnik',self.dictionary_of_secures)
        print('nova login lista',self.list_of_snames)
        print('nova cred lista',self.list_of_credentials)
        self.update()
#password generator          
class Generator(UserControl):
    def __init__(self):
        super().__init__()
        #the text field that will contain the generated password
        self.generated_password=ft.TextField(label="generated password")
    
    def build(self):
        self.tasks = ft.Column()
        #the view before you click on generate passsowrd button
        self.first_display_view=(
            ft.Column([
                ft.Text(value="Welcome to the password generator",size=50,text_align="LEFT"),
                ft.FilledButton(text="generate password",on_click=self.password_generator)
            ])
        )
        #the view after you click on the generate password button
        self.second_display_view=(
            ft.Column(
                visible=False,

                controls= [
                ft.Text(value="Welcome to the password generator",size=50,text_align="LEFT"),
                ft.FilledButton(text="generate password",on_click=self.password_generator),
                self.generated_password
                ]
            )
        )
        return ft.Column(controls=[self.first_display_view, self.second_display_view])
    #password generator
    def password_generator(self,e):
        self.first_display_view.visible=False
        self.second_display_view.visible=True
        #imported from the password generator file
        a=generate_password(length=12, include_digits=True, include_special_chars=True)
        self.generated_password.value=a
        self.update()


    
