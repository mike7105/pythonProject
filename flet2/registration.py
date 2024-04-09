import flet as ft
import sqlite3


def main(page: ft.Page):
    page.title = "TestApp"
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

        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_reg.text = 'Done!'
        page.update()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True

        page.update()

    def auth_user(e):
        db = sqlite3.connect("regapp.sqlite3")

        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE login = '{user_login.value}' and pass = '{user_pass.value}'")

        if cur.fetchone() is not None:
            user_login.value = ''
            user_pass.value = ''
            btn_auth.text = 'Auth!'

            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(
                    ft.NavigationDestination(icon=ft.icons.BOOK,
                                             label='Cabinet',
                                             selected_icon=ft.icons.BOOKMARK))

            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text('No such user!'))
            page.snack_bar.open = True
            page.update()

        db.commit()
        db.close()

    user_login = ft.TextField(label='Login', width=200, on_change=validate)
    user_pass = ft.TextField(label='Password', password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Add', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Athorizate', width=200, on_click=auth_user, disabled=True)

    # USer Cabinet

    users_list = ft.ListView(spacing=10, padding=20)

    # USer Cabinet End
    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    panel_register = ft.Row(
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
    )

    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Authorization'),
                    user_login,
                    user_pass,
                    btn_auth
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_cabinet = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Cabinet'),
                    users_list
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0:
            page.add(panel_register)
        elif index == 1:
            page.add(panel_auth)
        elif index == 2:
            users_list.controls.clear()

            db = sqlite3.connect("regapp.sqlite3")

            cur = db.cursor()
            cur.execute(f"SELECT * FROM users")
            res = cur.fetchall()

            if res is not None:
                for user in res:
                    print(user)
                    users_list.controls.append(ft.Row([
                        ft.Text(f'User {user[1]}'),
                        ft.Icon(ft.icons.VERIFIED_USER_ROUNDED)
                    ]))
            db.commit()
            db.close()
            page.add(panel_cabinet)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label="Register"),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER_OUTLINED, label="Authorizate")
        ], on_change=navigate
    )

    page.add(panel_register)


ft.app(target=main)  # , view=ft.AppView.WEB_BROWSER)
