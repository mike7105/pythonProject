import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "Регистрация"
    page.theme_mode = 'dark'  # light
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 400
    page.window_resizable = False

    def register(e):
        db = sqlite3.connect("regapp.sqlite3")

        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            login TEXT,
            pass TEXT
        )""")

        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_pass.value}')")

        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_reg.text = 'Done!'
        page.update()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
        else:
            btn_reg.disabled = True

        page.update()

    user_login = ft.TextField(label='Login', width=200, on_change=validate)
    user_pass = ft.TextField(label='Password', password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Add', width=200, on_click=register, disabled=True)

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                ft.Column(
                    [
                        ft.Text('Registration'),
                        user_login,
                        user_pass,
                        btn_reg
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )


ft.app(target=main)  # , view=ft.AppView.WEB_BROWSER)
