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
class Task(ft.UserControl):
    def __init__(self, task_name,task_delete):
        super().__init__()
        self.task_name = task_name
        self.task_delete = task_delete

    def build(self):
        self.first_task = TextField(hint_text="Enter your master password here",password=True,can_reveal_password=True, expand=True)
        self.tasks = ft.Column()
        self.second_task = ft.TextField(hint_text="CORRECT", expand=True)
        
        self.display_task = ft.Checkbox(value=False, label=self.task_name)
        self.edit_name = ft.TextField(expand=1)
        #self.first_task=TextField(hint_text="Enter your master password here",password=True,can_reveal_password=True, expand=True)

        self.first_view= ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.first_task,
                ft.FloatingActionButton(icon=ft.icons.INPUT, on_click=self.add_clicked)
            ],
        )
        self.second_view= ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.second_task,
                ft.FloatingActionButton(icon=ft.icons.INPUT, on_click=self.add_clicked)
            ],
        )

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
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

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.first_view,self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def add_clicked(self, e):
        #task = Task(self.new_task.value, self.task_delete)
        self.first_view.visible = False
        self.second_view.visible = True
        #self.tasks.controls.append(task)
        #self.new_task.value = ""
        self.update()

    def delete_clicked(self, e):
        self.task_delete(self)

class PW_UI(UserControl):
    def build(self):
        self.first_task = TextField(hint_text="Enter your master password here",password=True,can_reveal_password=True, expand=True)
        self.tasks = ft.Column()
       
        self.first_view= ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.first_task,
                ft.FloatingActionButton(icon=ft.icons.INPUT, on_click=self.check_mpass)
            ],
        )
        
        
        
        # application's root control (i.e. "view") containing all other controls
        return ft.Column(controls=[self.first_view,self.tasks])
    
    def add_mpass(self):
        pass
    def check_mpass(self,e):
      
        if self.first_task.value=="Jana123":
            correct=True
        else:
            correct=False

        if correct:
            self.categories_view=ft.Row(
                
                [ 
                    ft.Container(
                        content=ft.Column([

                            ft.Text(value="categories",size=18,color=ft.colors.BLUE_200,font_family="Consolas"), ft.FilledButton(text="logins",icon_color=ft.colors.RED)
                        ]),
                        bgcolor=ft.colors.RED,
                        alignment=ft.alignment.center,
                        height=650,
                        width=300,
                        padding=0
                        
                    ),
                    ft.Container(
                        content=ft.TextField(value="contents"),
                        bgcolor=ft.colors.GREEN,
                        alignment=ft.alignment.center,
                        height=650,
                        width=940,
                        #extend=True   
                    )
                ]
                )
            
            # self.contents_view=ft.Column([
            #     ft.Container(
            #             content=ft.TextField(value="contents"),
            #             bgcolor=ft.colors.BLUE,
            #             alignment=ft.alignment.center,
            #             height=100,
            #             padding=0
                        
            #         )
            # ]


            # )
                
                    
            

            self.first_view.visible=False
            
            #self.tasks.controls.append(self.second_view)
            self.tasks.controls.append(self.categories_view)
            #self.tasks.controls.append(self.contents_view)
            print("appended")
            
            self.update()
        else:
            self.wrong_task=ft.Text(value="The value you entered is wrong, try again...",color=ft.colors.RED)
            self.wrong_view=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.wrong_task  
                ],

            )
            self.tasks.controls.append(self.wrong_view)
            self.update()

    
    
        


def main(page: ft.Page):
    page.title = "Password Manager"
    page.vertical_alignment="center"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    pwm = PW_UI()

    # add application's root control to the page
    page.add(pwm)

ft.app(target=main)
