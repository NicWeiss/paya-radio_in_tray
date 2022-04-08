import os
import threading
import webbrowser
from time import sleep

import pystray
from backend.lib.helpers import get_ip
from notifypy import Notify
from PIL import Image
from pystray import MenuItem as item


YA_ICON_PATH = f"{os.path.dirname(__file__)}/../assets/icon.png"


class TrayMenu():

    def __init__(self, config, action_like, action_dislike):
        self.config = config
        self.player = PlayerStub()
        self.action_like = action_like
        self.action_dislike = action_dislike

        self.tray_menu = threading.Thread(name='YaTrayMenu', target=self.create_menu)
        self.tray_menu.setDaemon(True)
        self.tray_menu.start()

    def set_player(self, player):
        self.player = player

    def create_menu(self):
        image = Image.open(YA_ICON_PATH)
        menu = (
            item('Next', self.next),
            item('Play / Pause', self.pause),
            item(' ', self.stub),
            item('Like', self.action_like),
            item('Dislike', self.dislike),
            item(' ', self.stub),
            item('About track', self.about_track),
            item('Open wep player', self.open_web_player),
            item(' ', self.stub),
            item('Exit', self.close_app)
        )
        self.icon = pystray.Icon("Ya Radio", image, "Ya Radio", menu)
        self.icon.run()

    def dislike(self):
        self.action_dislike()
        self.notify_track_title()

    def next(self):
        self.player.next(self.notify_track_title)

    def pause(self):
        self.player.pause()

    def notify_track_title(self, sleep_time=1):
        sleep(sleep_time)

        track = self.player.get_track()
        title = track['title']
        artists = ''.join([artist['name'] for artist in track['artists']])

        notification = Notify()
        notification.title = title
        notification.message = artists
        print(self.player.get_cover_path())
        notification.icon = self.player.get_cover_path()
        notification.send()

    def about_track(self):
        self.notify_track_title(0)

    def open_web_player(self):
        webbrowser.open(f'http://{get_ip()}:{self.config["frontend"]["port"]}')

    def close_app(self):
        os.system(
            'for pid in $(ps aux | grep gunicorn |grep ya.radio | awk \'{print $2}\'); do kill -9 $pid; done'
        )

    def stub(self):
        pass


class PlayerStub:
    def pause(self, *args, **kwargs):
        pass

    def next(self, *args, **kwargs):
        pass

    def play(self, *args, **kwargs):
        pass

    def get_cover_path(self, *args, **kwargs):
        return YA_ICON_PATH

    def get_track(self, *args, **kwargs):
        return {
            'title': 'Track',
            'artists': [{'name': 'Not loaded'}]
        }
