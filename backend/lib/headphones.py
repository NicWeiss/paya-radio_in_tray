import threading
from time import sleep
from pynput import keyboard

from backend.lib.helpers import shell
from backend.lib.notify import Notify


class HeadphonesObserver:
    def __init__(self, player):
        self.player = player
        self.headphones_state = None
        self.tray_menu = threading.Thread(name='YaHeadphonesObserver', target=self.observer)
        self.tray_menu.setDaemon(True)
        self.tray_menu.start()

        self.listner = threading.Thread(name='YaHeadphonesKeyListner', target=self.key_listner)
        self.listner.setDaemon(True)
        self.listner.start()

    def observer(self):
        while True:
            self.check_headphones()
            sleep(2)

    def check_headphones(self):
        result = shell('pactl list sinks | grep bluez_sink | head -n 1')

        if self.headphones_state is not None:
            if bool(result):
                if not self.headphones_state:
                    if not self.player.is_playing:
                        self.player.play()

                    Notify().about_track(self.player.get_track(), self.player.get_cover_path())
            else:
                if self.headphones_state and self.player.is_playing:
                    self.player.pause()
                    Notify().pause_playing('Наушники отключены')

        self.headphones_state = bool(result)

    def key_listner(self):
        # Collect events until released
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def on_press(self, key):
        try:
            _ = key.char
        except AttributeError:
            if str(key) == 'Key.media_play_pause':
                print('[HEADPHONES] Pause')
                self.player.pause()

            if str(key) == 'Key.media_next':
                print('[HEADPHONES] Next track')
                self.player.next()

            if str(key) == 'Key.media_previous':
                print('[HEADPHONES] Repeate track')
                self.player.repeate()
