import flet as ft

def main(page: ft.Page):
    page.title = "Text editor"
    page.theme_mode = 'dark'  # light
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 500
    page.window_height = 700
    page.window_resizable = False
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    path = ''

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    def pick_result(e: ft.FilePickerResultEvent):
        nonlocal path
        if not e.files:
            selected_files.value = 'None choosen'
        else:
            selected_files.value = ''

            for el in e.files:
                path = el.path

            with open(path, 'r') as f:
                text_field.value = f.read()

        page.update()

    def save_file(e):
        nonlocal path
        with open(path, 'w') as f:
            f.write(text_field.value)

        text_field.value = ''
        save_button.text = 'Done!'

        page.update()

    text_field = ft.TextField(label="File text", width=460, height=500, multiline=True)
    pick_dialog = ft.FilePicker(on_result=pick_result)
    page.overlay.append(pick_dialog)
    selected_files = ft.Text()
    save_button = ft.FilledButton('Save', on_click=save_file)

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                ft.Text('Pick files', size=25, weight=ft.FontWeight.W_500)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.ElevatedButton(
                    "Choose file", icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_dialog.pick_files(allow_multiple=False))
            ],
            alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([text_field]),
        ft.Row([save_button]),
        ft.Row([selected_files]),

    )


ft.app(target=main)  # , view=ft.AppView.WEB_BROWSER)
