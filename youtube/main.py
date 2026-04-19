"""скачивает видео с youtube
https://pytube3.readthedocs.io/en/latest/user/quickstart.html"""
# from pytube import Playlist
from pytube import YouTube


if __name__ == '__main__':
    # YouTube('https://youtu.be/6KwLpnCdQiA').streams.first().download(r"C:\Users\25430\Downloads\new")
    yt = YouTube('https://www.youtube.com/watch?v=6KwLpnCdQiA')
    print(yt.streams.all())



          # .streams.get_highest_resolution().download(r"C:\Users\25430\Downloads\new"))

    # p = Playlist('https://youtu.be/6KwLpnCdQiA')
    # print(f'Downloading: {p.title}, videos: {p.length}')
    # for i, video in enumerate(p.videos):
    #     # video.streams.first().download()
    #     ys = video.streams.get_highest_resolution()
    #     print(f'{i+1} Downloading: {ys.title}')
    #     ys.download(r"C:\Users\25430\Downloads\new")
