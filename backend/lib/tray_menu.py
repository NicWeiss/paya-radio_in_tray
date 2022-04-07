import os
import threading
import webbrowser
from time import sleep

import pystray
from backend.lib.helpers import get_ip
from PIL import Image
from pystray import MenuItem as item


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
        image = Image.open(f"{os.path.dirname(__file__)}/../assets/icon.png")
        menu = (
            item('Next', self.next),
            item('Play / Pause', self.player.pause),
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

    def notify_track_title(self, sleep_time=1):
        sleep(sleep_time)
        track = self.player.get_track()
        title = track['title']
        artists = ''.join([artist['name'] for artist in track['artists']])

        self.icon.notify(f'{title} - {artists}')

    def about_track(self):
        self.notify_track_title(0)

    def open_web_player(self):
        webbrowser.open(f'http://{get_ip()}:{self.config["frontend"]["port"]}')

    def close_app(self):
        os.system('kill $(ps ax | grep gunicorn | grep 7778 | grep S+ | cut -d " " -f2)')

    def stub(self):
        pass


class PlayerStub:
    def pause(self, *args, **kwargs):
        pass

    def next(self, *args, **kwargs):
        pass

    def get_track(self, *args, **kwargs):
        return {
            'title': 'Track',
            'artists': [{'name': 'Not loaded'}]
        }
