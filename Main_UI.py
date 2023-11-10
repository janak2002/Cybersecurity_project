#import libraries
import flet as ft
from AES_finalenc_masterenc import PasswordManager
import os
import flet as ft
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
from UI_classes import Logins
from UI_classes import Card
from UI_classes import Secure
from UI_classes import Generator


#class that will be the entire UI
class PW_UI(UserControl):
    def __init__(self,dictionary_of_logins,list_of_sites,list_of_creds_login,list_of_cred_cards,line_lengths,dictionary_of_cards,list_of_names,dictionary_of_secures,list_of_snames,list_of_cred_secures):
        super().__init__()
        self.dictionary_of_logins=dictionary_of_logins
        self.list_of_site=list_of_sites
        self.dictionary_of_cards=dictionary_of_cards
        self.list_of_names=list_of_names
        self.list_of_credentials_login=list_of_creds_login
        self.list_of_credentials_cards=list_of_cred_cards
        self.line_lengths=line_lengths
        self.dictionary_of_secures=dictionary_of_secures
        self.list_of_snames=list_of_snames
        self.list_of_credentials_secures=list_of_cred_secures
        self.content=Logins(self.dictionary_of_logins,self.list_of_site,self.list_of_credentials_login,self.line_lengths)
        
        #what appears when you unlock the manager
        self.clicked_view=(
            ft.Row(
            
            [ 
                ft.Container(
                    content=ft.Column([
                        #on the left of the screen the categories will be
                        ft.Text(value=""),
                        ft.Text(value="Categories",size=25,font_family="Kanit"),
                        ft.Text(value=""),
                        ft.FilledButton(text="logins",icon_color=ft.colors.BLUE_600,on_click=self.logins_open),
                        ft.Text(value=""),
                        ft.FilledButton(text="cards",icon_color=ft.colors.BLUE_600,on_click=self.cards_open),ft.Text(value=""),
                        ft.FilledButton(text="secure notes",icon_color=ft.colors.BLUE_600,on_click=self.secure_open),ft.Text(value=""),
                        ft.FilledButton(text="generator",icon_color=ft.colors.BLUE_600,on_click=self.generator_open)
                        
                    ]),
                    bgcolor=ft.colors.GREY_900,
                    alignment=ft.alignment.center,
                    height=650,
                    width=150,
                    padding=0
                    
                ),
                ft.Container(
                    #self.content will be an instance of one of the classes from the UI_classes.py file
                    content= self.content,
                    bgcolor=ft.colors.GREY_800,
                    alignment=ft.alignment.top_left,
                    height=650,
                    width=1080,
                    padding=20,
                    expand=True   
                )
            ]
            )
        )
        self.clicked_view.visible=False
        
       
    def build(self):
        #asking for input of the master password
        self.first_task = TextField(hint_text="Enter your master password here",password=True,can_reveal_password=True, expand=True)
        pw=PasswordManager()
        self.tasks = ft.Column()

        self.key=pw.generate_key('myfunkey.key')
        #get the master password if it exists
        self.mpass=pw.get_master_password()

        #decode the master password 
        self.mpass=self.mpass.decode("utf-8")
        print(self.mpass)
       
        #the first view checks if the password the user inputs is the same as the product of get_password function
        self.first_view= ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.first_task,
                ft.FloatingActionButton(icon=ft.icons.INPUT, on_click=self.check_mpass)
            ],
        )
       
        
        
        
        # application's root control (i.e. "view") containing all other controls
        return ft.Column(controls=[self.first_view,self.tasks,self.clicked_view])
    
    #checks of the masterpassword is correct

    def check_mpass(self,e):
        
        if self.first_task.value==self.mpass:
            correct=True
        else:
            correct=False
        #if it's wrong make the wrong_task that shall be displayed on the screen
        self.wrong_task=ft.Text(value="The value you entered is wrong, try again...",color=ft.colors.RED)
        #make the wrong view
        self.wrong_view=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.wrong_task  
            ],

        )
        if correct:
            #if it's correct make the first view that welcomes the user to the manager and shows categories
            self.begin_view=ft.Row(
                [ 
                    ft.Container(
                        content=ft.Column([
                            ft.Text(value=""),
                            ft.Text(value="Categories",size=25,font_family="Kanit"),
                            ft.Text(value=""),
                            ft.FilledButton(text="logins",icon_color=ft.colors.BLUE_600,on_click=self.logins_open),
                            ft.Text(value=""),
                            ft.FilledButton(text="cards",icon_color=ft.colors.BLUE_600,on_click=self.cards_open),ft.Text(value=""),
                            ft.FilledButton(text="secure notes",icon_color=ft.colors.BLUE_600,on_click=self.secure_open),ft.Text(value=""),
                            ft.FilledButton(text="generator",icon_color=ft.colors.BLUE_600,on_click=self.generator_open)
                            
                        ]),
                        bgcolor=ft.colors.GREY_900,
                        alignment=ft.alignment.center,
                        height=650,
                        width=150,
                        padding=0
                        
                    ),
                    ft.Container(
                    
                        content= ft.Text(value="Welcome to your password manager",size=50,font_family="Kanit"),
                        bgcolor=ft.colors.GREY_800,
                        alignment=ft.alignment.center,
                        height=650,
                        width=1080,
                        padding=20,
                        expand=True   
                    )
                ]
                )
            
            #disable the first view
            self.first_view.visible=False
            self.begin_view.visible=True
            
            #remove self.first_view from the controls
            if len(self.tasks.controls) !=0:

                self.tasks.controls.pop()
            
            
            #append the begin view to the controls
            self.tasks.controls.append(self.begin_view)
            
            print("appended")
            
            self.update()
        else:
            #if the password is wrong make the wrong_view visible
            self.first_task.value=""
            
            self.tasks.controls.append(self.wrong_view)
            self.update()
        
        return self.dictionary_of_cards
    #new_view - function that handles the user's clicks on different categories
    def new_view(self):
         if self.clicked_view in self.tasks.controls:
            self.tasks.controls.remove(self.clicked_view)
        #clicked_view is what appears on screen when a certain category is clicked
         self.clicked_view=(
              ft.Row(
                
                [ 
                    ft.Container(
                        content=ft.Column([
                            ft.Text(value=""),
                            ft.Text(value="Categories",size=25,font_family="Kanit"),
                            ft.Text(value=""),
                            ft.FilledButton(text="logins",icon_color=ft.colors.BLUE_600,on_click=self.logins_open),
                            ft.Text(value=""),
                            ft.FilledButton(text="cards",icon_color=ft.colors.BLUE_600,on_click=self.cards_open),ft.Text(value=""),
                            ft.FilledButton(text="secure notes",icon_color=ft.colors.BLUE_600,on_click=self.secure_open),ft.Text(value=""),
                            ft.FilledButton(text="generator",icon_color=ft.colors.BLUE_600,on_click=self.generator_open)
                            
                        ]),
                        bgcolor=ft.colors.GREY_900,
                        alignment=ft.alignment.center,
                        height=650,
                        width=150,
                        padding=0
                        
                    ),
                    ft.Container(
                        #as explained above self.content is changeable depending on the category viewed
                        content= self.content,
                        bgcolor=ft.colors.GREY_800,
                        alignment=ft.alignment.top_left,
                        height=650,
                        width=1080,
                        padding=20,
                        expand=True   
                    )
                ]
                )
         )
         #make the clicked_view visible and add it to the controls
         self.clicked_view.visible=True
         self.tasks.controls.append(self.clicked_view)
        
         self.update()
    #if logins is clicked self.content is an instance of a login class, call new_view to update page
    def logins_open(self,e):
        print("LOGINS")
        self.begin_view.visible=False
        
        self.content=Logins(self.dictionary_of_logins,self.list_of_site,self.list_of_credentials_login,self.line_lengths)
        
        self.new_view()
    #if cards is clicked self.content is an instance of a card class, call new_view to update page
    def cards_open(self,e):
         self.begin_view.visible=False
        
         print('CARDS')
         self.content=Card(self.dictionary_of_cards,self.list_of_names,self.list_of_credentials_cards,self.line_lengths)
         
         self.new_view()
    #if secure notes is clicked self.content is an instance of a secure class, call new_view to update page
    def secure_open(self,e):
         self.begin_view.visible=False
        
         print('Secures')
         self.content=Secure(self.dictionary_of_secures,self.list_of_snames,self.list_of_credentials_secures,self.line_lengths)
         
         self.new_view()
    #if password generator is clicked self.content is an instance of a generator class, call new_view to update page
    def generator_open(self,e):
         self.begin_view.visible=False
         self.content=Generator()
         self.new_view()


   
    
#clear file
def clear_file(file_path):
        with open(file_path, 'w'):  # 'wb' for binary files
            pass   

#in case the master doesn't exist, here's a function that creates it - it returns the password in the terminal if it already exists
#this was for testing purposes and need a few lines of code to be fully implemented with the current version of encryption file and
#the classes file
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


         
        

#main
def main(page: ft.Page):
    page.title = "Password Manager"
    page.bgcolor=ft.colors.GREY_900
    page.vertical_alignment="center"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
   
    list_sites=[]
    line_lengths=[]
    list_cred_log=[]
    list_cred_cards=[]
    list_names=[]
    dict2={}
    page.update()
    dict={}
    dict3={}
    list_snames=[]
    list_cred_secures=[]
    # create application instance
    pwm = PW_UI(dict,list_sites,list_cred_log,list_cred_cards,line_lengths,dict2,list_names,dict3,list_snames,list_cred_secures)
   

    print(dict)
    #for setting the master password - currently disabled and has to be a bit tweaked to be implemented properly
    #master_password_set(master_password.bin,pw)
    # add application's root control to the page
    page.add(pwm)

ft.app(target=main)
