import os
import threading
from time import sleep

import pystray
from PIL import Image
from pystray import MenuItem as item


class TrayMenu():

    def __init__(self, player, action_like, action_dislike):
        self.player = player
        self.action_like = action_like
        self.action_dislike = action_dislike

        self.tray_menu = threading.Thread(name='YaTrayMenu', target=self.create_menu)
        self.tray_menu.setDaemon(True)
        self.tray_menu.start()

    def create_menu(self):
        image = Image.open(f"{os.path.dirname(__file__)}/../assets/icon.png")
        menu = (
            item('Next', self.next),
            item('Play / Pause', self.player.pause),
            item(' ', self.stub),
            item('Like', self.action_like),
            item('Dislike', self.dislike),
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

    def notify_track_title(self):
        sleep(1)
        track = self.player.get_track()
        title = track['title']
        artists = ''.join([artist.name for artist in track.artists])

        self.icon.notify(f'{title} - {artists}')

    def close_app(self):
        os.system('kill $(ps ax | grep gunicorn | grep 7778 | grep S+ | cut -d " " -f1)')

    def stub(self):
        pass
