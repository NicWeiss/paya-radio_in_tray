import threading
from time import sleep

import vlc

from backend.lib.helpers import clear_lock, is_locked, set_lock
from backend.lib.loader import Loader
from backend.lib.notify import Notify


class Player():
    def __init__(self, radio, station):
        self.radio = radio
        self.loader = Loader()
        self.player = vlc.MediaPlayer()
        self.start_last_track()
        clear_lock('next')

        self.next_track_file = None
        self.track_history = []

        first_track = radio.start_radio(station, '')

        self.loader.download(first_track)
        self.next_track_file = self.current_track_file = self.loader.get_track_path(first_track)

    def start_last_track(self):
        try:
            self.track = self.loader.restore_track(self.radio.client)

            if not self.track:
                return

            self.current_track_file = self.loader.get_track_path(self.track)
            self.play(cold_boot=True)
        except Exception as exc:
            raise exc

        self.current_track_file = None

    def play(self, cold_boot=False):
        if self.is_playing:
            return True

        if self.is_paused:
            return self.pause()

        if track := self.radio.get_current_track():
            self.track = track

        track_title = self.track['title']
        artist_name = self.track['artists'][0]['name']

        media = vlc.Media(f'file://{self.current_track_file}')
        self.player.set_media(media)
        self.player.play()

        print(f'[Playing] {artist_name}: {track_title}')
        Notify().about_track(self.track, self.get_cover_path())

        if cold_boot:
            return

        self.loader.store_track(self.track)
        self.next_track_file = None
        download = threading.Thread(name='Continious playing', target=self.load_next_track)
        download.start()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def load_next_track(self):
        is_track_loaded = False
        self.next_track_file = None

        while is_track_loaded == False:
            if track := self.radio.play_next():
                is_track_loaded = self.loader.download(track)
            else:
                print('Can\'t get next track')

        self.next_track_file = self.loader.get_track_path(track)

    def next(self, callback=None):
        next_thread = threading.Thread(name='Start next track',
                                       target=self._next_as_background, args=[callback])
        next_thread.start()

    def _next_as_background(self, callback):
        if is_locked('next'):
            return

        set_lock('next')
        self.track_history.append((self.track, self.loader.open_history_cover(self.track.id)))
        self.stop()

        while self.next_track_file == None:
            print('Waiting next track')
            sleep(1)

        self.loader.clear_data_by_id(self.track.id)
        self.current_track_file = self.next_track_file
        self.play()

        if callback:
            callback()

        clear_lock('next')
        exit(0)

    def get_track(self):
        return self.track

    def get_cover(self):
        return self.loader.open_cover(self.track.id)

    def get_cover_path(self):
        return self.track and self.loader.get_cover_path(self.track.id)

    def get_state(self):
        return str(self.player.get_state()).split('.')[1]

    def get_current_playtime(self):
        return int(self.player.get_time())

    def get_track_duration(self):
        return int(self.track.duration_ms)

    def get_history(self):
        return self.track_history

    @property
    def is_opening(self):
        return bool(self.get_state() == 'Opening')

    @property
    def is_buffering(self):
        return bool(self.get_state() == 'Buffering')

    @property
    def is_playing(self):
        return bool(self.get_state() == 'Playing')

    @property
    def is_paused(self):
        return bool(self.get_state() == 'Paused')

    @property
    def is_stopped(self):
        return bool(self.get_state() == 'Stopped')

    @property
    def is_ended(self):
        return bool(self.get_state() == 'Ended')

    @property
    def is_error(self):
        return bool(self.get_state() == 'Error')
