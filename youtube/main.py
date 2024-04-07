"""скачивает видео с youtube
https://pytube.io/en/latest/api.html"""
from pytube import Playlist

if __name__ == '__main__':
    p = Playlist('https://www.youtube.com/watch?v=99RhirZkT7s&list=PLC8azx2wuTWjsaLbf6uPUKxRoO-A-y5wb')
    print(f'Downloading: {p.title}, videos: {p.length}')
    for i, video in enumerate(p.videos):
        # video.streams.first().download()
        ys = video.streams.get_highest_resolution()
        print(f'{i+1} Downloading: {ys.title}')
        ys.download(r"N:\мультфильмы\лёва")
