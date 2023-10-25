import flet as ft

class Passwordmanager(ft.UserControl):
    def build(self):
        self.new_task = ft.TextField(hint_text="What Is Your Password", password = True, can_reveal_password = True, expand=True)
        self.tasks = ft.Column()

        # Root control
        return ft.Column(
            width=500,
            controls=[
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(icon=ft.icons.INPUT, on_click=self.add_clicked),
                    ],
                ),
                self.tasks,
            ],
        )

    def add_clicked(self, e):
        self.new_task.value = ""
        self.update()


def main(page: ft.Page):
    page.title = "Password Manager"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    pwm = Passwordmanager()

    # add application's root control to the page
    page.add(pwm)

ft.app(target=main)
