import os
import threading
import webbrowser

import pystray
from backend.lib.helpers import close_app, get_ip
from PIL import Image
from pystray import Menu
from pystray import MenuItem as item

from .notify import Notify


YA_ICON_PATH = f"{os.path.dirname(__file__)}/../assets/icon.png"


class TrayMenu():

    def __init__(self, config, action_like, action_dislike, stations):
        self.config = config
        self.stations = stations
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
            item('About station', self.about_station),
            item(' ', self.stub),
            item('Stations', Menu(
                *[item(s['name'], self.change(s['id'], s['name'])) for s in self.stations['rec']],
                item(' ', self.stub),
                *[item(cat, Menu(
                    *[item(s['name'], self.change(s['id'], s['name'])) for s in self.stations['all'][cat]]
                )) for cat in self.stations['all']]
            )),
            item('Open web player', self.open_web_player),
            item(' ', self.stub),
            item('Exit', close_app)
        )
        self.icon = pystray.Icon("Ya Radio", image, "Ya Radio", menu)
        self.icon.run()

    def dislike(self):
        self.action_dislike()

    def next(self):
        self.player.next()

    def pause(self):
        if self.player.is_playing:
            Notify().pause_playing()
        else:
            Notify().about_track(self.player.get_track(), self.player.get_cover_path())

        self.player.pause()

    def about_track(self):
        Notify().about_track(self.player.get_track(), self.player.get_cover_path())

    def about_station(self):
        Notify().info(self.player.get_station(), 'Радио')

    def open_web_player(self):
        webbrowser.open(f'http://{get_ip()}:{self.config["frontend"]["port"]}')

    def change(self, station_id, name):
        def inner():
            print(station_id)
            self.player.change_station(station_id, name)

        return inner

    def stub(self):
        pass


class PlayerStub:
    def default_info(self):
        Notify().info('Идёт заргузка, ожидайте')

    def pause(self, *args, **kwargs):
        self.default_info()

    def next(self, *args, **kwargs):
        self.default_info()

    def play(self, *args, **kwargs):
        self.default_info()

    def change_station(self, *args, **kwargs):
        self.default_info()

    def get_cover_path(self, *args, **kwargs):
        return YA_ICON_PATH

    def get_track(self, *args, **kwargs):
        return {
            'title': 'Track',
            'artists': [{'name': 'Not loaded'}]
        }

    def get_station(self, *args, **kwargs):
        return 'Ещё не загружено'
