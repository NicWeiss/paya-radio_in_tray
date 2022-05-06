import os

from notifypy import Notify as SystemNotify


class Notify:

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
