import threading
from time import sleep

from backend.lib.helpers import shell
from backend.lib.notify import Notify


class HeadphonesObserver:
    def __init__(self, player):
        self.player = player
        self.headphones_state = None
        self.tray_menu = threading.Thread(name='YaHeadphonesObserver', target=self.observer)
        self.tray_menu.setDaemon(True)
        self.tray_menu.start()

    def observer(self):
        while True:
            self.check_headphones()
            sleep(2)

    def check_headphones(self):
        result = shell('pacmd list-sinks | grep bluez_sink | head -n 1')

        if self.headphones_state is not None:
            if bool(result):
                if not self.headphones_state:
                    self.player.play()
                    Notify().about_track(self.player.get_track(), self.player.get_cover_path())
            else:
                if self.headphones_state:
                    self.player.pause()
                    Notify().pause_playing()

        self.headphones_state = bool(result)
