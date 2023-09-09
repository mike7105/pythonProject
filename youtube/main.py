"""скачивает видео с youtube
https://pytube.io/en/latest/api.html"""
from pytube import Playlist

if __name__ == '__main__':
    # p = Playlist('https://www.youtube.com/watch?v=B0Bud-FBWAM&list=PLbdq7Jys9Gmxkty3BTtRo3bTurSVlQfCr')
    # p = Playlist('https://www.youtube.com/watch?v=V5SJJ_6FWlM&list=PLbdq7Jys9GmwGFSWlljtR1Y0QGe3pY8HE')
    # p = Playlist('https://www.youtube.com/watch?v=SrmUFlOt56c&list=PLbdq7Jys9GmzI9iajCUZTZe34yr9oy9au')
    p = Playlist('https://www.youtube.com/watch?v=T2102Wdb9w0&list=PLbdq7Jys9GmzkBX06eoiBbgvAq2RdLwG6')
    print(f'Downloading: {p.title}, videos: {p.length}')
    for i, video in enumerate(p.videos):
        # video.streams.first().download()
        ys = video.streams.get_highest_resolution()
        print(f'{i+1} Downloading: {ys.title}')
        ys.download(r"N:\Мультфильмы\Гордон\сезон 4")
