import os
import threading
import webbrowser

import pystray
from backend.lib.helpers import close_app, get_ip
from PIL import Image
from pystray import Menu
from pystray import MenuItem as item
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .notify import Notify


YA_ICON_PATH = f"{os.path.dirname(__file__)}/../assets/icon.png"


class TrayMenu():

    def __init__(self, config, action_like, action_dislike, stations):
        self.config = config
        self.stations = stations
        self.player = PlayerStub()
        self.action_like = action_like
        self.action_dislike = action_dislike
        self.action_id = 0

        self.tray_menu = threading.Thread(name='YaTrayMenu', target=self.create_menu)
        self.tray_menu.setDaemon(True)
        self.tray_menu.start()

    def set_player(self, player):
        self.player = player

    def create_menu(self):
        actions = {}

        def add_action(menu, name, action=None):
            actions[self.action_id] = QAction(f"{name}")
            if action:
                actions[self.action_id].triggered.connect(action)
            menu.addAction(actions[self.action_id])
            self.action_id = self.action_id + 1

        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

        # Create the icon
        icon = QIcon(YA_ICON_PATH)

        # Create the tray
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        # Create the menu
        menu = QMenu()

        add_action(menu=menu, name="Next", action=self.next)
        add_action(menu=menu, name="Play / Pause", action=self.pause)
        add_action(menu=menu, name=" ")
        add_action(menu=menu, name="Like", action=self.action_like)
        add_action(menu=menu, name="Dislike", action=self.dislike)
        add_action(menu=menu, name=" ",)
        add_action(menu=menu, name="About track", action=self.about_track)
        add_action(menu=menu, name="About station", action=self.about_station)
        add_action(menu=menu, name=" ")

        # stations_menu = QMenu("Stations", menu)
        # for line in [item(s['name'], self.change(s['id'], s['name'])) for s in self.stations['rec']]:
        #     add_action(stations_menu, line)

        # for line in [item(cat, Menu(
        #             *[item(s['name'], self.change(s['id'], s['name'])) for s in self.stations['all'][cat]]
        #         )) for cat in self.stations['all']]:
        #     add_action(stations_menu, line)

        # menu.addMenu("Stations", stations_menu)
        add_action(menu=menu, name="Open web player", action=self.open_web_player)
        add_action(menu=menu, name=" ")
        add_action(menu=menu, name="Exit", action=close_app)

        # Add the menu to the tray
        tray.setContextMenu(menu)

        app.exec_()

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
    is_playing = False

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
