"""Интерфейс загрузки в ютуб"""

from time import time

from customtkinter import *
from pytube import YouTube, exceptions


# Функция скачивания видео
def download_video(entry_field: str, d_loc: str) -> None:
    """
    скачивает видео по ссылке в указанную папку
    :param str entry_field:  ссылк ана видео
    :param str d_loc: папка сохранения
    """
    if not os.path.exists(d_loc):
        os.mkdir(d_loc)
    try:
        start_time = time()
        YouTube(entry_field).streams.get_highest_resolution().download(d_loc)
        end_time = time()

        # Отображение времени загрузки в новом окне
        popup = CTk()
        popup.title("Download Status")
        popup.resizable(False, False)
        popup.geometry("200x100")
        popup.grid_columnconfigure(0, weight=1)
        # noinspection PyTypeChecker
        popup.grid_rowconfigure((0, 1), weight=1)

        msg = StringVar()
        msg.set(f"Download successful!\nTotal time taken: {round(end_time - start_time, 3)} seconds")

        label = CTkLabel(popup, text=msg.get())
        label.grid(row=0, column=0)

        button = CTkButton(popup, text="OK", command=popup.destroy)
        button.grid(row=1, column=0)

        popup.mainloop()

    except exceptions.RegexMatchError:
        # Если есть недействительная или пустая ссылка, отображается сообщение об ошибке.
        error = CTk()
        error.title("Error")
        error.resizable(False, False)
        error.geometry("300x100")
        # noinspection PyTypeChecker
        error.grid_rowconfigure((0, 1), weight=1)
        error.grid_columnconfigure(0, weight=1)

        error_label = CTkLabel(error, text="Please enter a valid YouTube link")
        error_label.grid(row=0, column=0)

        button = CTkButton(error, text="OK", command=error.destroy)
        button.grid(row=1, column=0)

        error.mainloop()


def initMain() -> None:
    """
    Инициализация макета приложения
    """

    master = CTk()
    master.title("YouTube Downloader")
    # noinspection PyTypeChecker
    master.grid_rowconfigure((0, 1, 2), weight=1)
    # noinspection PyTypeChecker
    master.grid_columnconfigure(1, weight=1)
    master.geometry("800x150")
    master.resizable(True, False)

    CTkLabel(master, text="Enter YouTube video URL:").grid(row=0, column=0, sticky="W", padx=5)
    entry = CTkEntry(master)
    entry.grid(row=0, column=1, sticky="EW", padx=5)

    CTkLabel(master, text="Enter folder to save:").grid(row=1, column=0, sticky="W", padx=5)
    download_location = CTkEntry(master)
    download_location.grid(row=1, column=1, sticky="EW", padx=5)

    CTkButton(master, text='Choose folder',
              command=lambda:
              download_location.insert(0, filedialog.askdirectory(parent=master))).grid(row=2, column=0)

    CTkButton(master, text='Download',
              command=lambda *args:
              download_video(entry.get(), download_location.get())).grid(row=2, column=1)

    master.mainloop()


if __name__ == '__main__':
    set_appearance_mode("System")
    set_default_color_theme("blue")
    initMain()
