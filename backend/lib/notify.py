import os

from notifypy import Notify as SystemNotify


class Notify:

    def error(self, message):
        cover = f"{os.path.dirname(__file__)}/../assets/error.png"
        self._notify('Ошибка', message, cover)

    def success(self, message):
        cover = f"{os.path.dirname(__file__)}/../assets/success.png"
        self._notify('Успех', message, cover)

    def info(self, message, title='Инфо'):
        cover = f"{os.path.dirname(__file__)}/../assets/icon.png"
        self._notify(title, message, cover)

    def about_track(self, track, cover):
        if not track:
            return

        title = track['title']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        self._notify(title, artists, cover)

    def pause_playing(self, message=''):
        title = 'Воспроизведение остановлено'
        cover = f"{os.path.dirname(__file__)}/../assets/pause.png"
        self._notify(title, message, cover)

    def _notify(self, title, message, cover):
        notification = SystemNotify()
        notification.title = title
        notification.message = message
        notification.icon = cover
        notification.send()
