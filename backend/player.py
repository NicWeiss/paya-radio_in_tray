import threading
from time import sleep

import vlc

from backend.lib.helpers import clear_lock, is_locked, set_lock
from backend.lib.loader import Loader
from backend.lib.notify import Notify


class Player():
    def __init__(self, radio, station_id, lastfm):
        self.lastfm = lastfm
        self.radio = radio
        self.loader = Loader()
        self.player = vlc.MediaPlayer()
        self.start_last_track()
        clear_lock('next')

        self.next_track_file = None
        self.track_history = []
        self.station_info = {}

        self.change_station(station_id, name='Моя волна', is_immediately_play=False)

    def change_station(self, station_id, name='', is_immediately_play=True):
        first_track = None

        if is_immediately_play:
            self.stop()

        try:
            first_track = self.radio.start_radio(station_id, '')
        except Exception as exc:
            err_message = 'Ошибка при запуске радиостанции'
            Notify().error(err_message)
            print(err_message)
            print(exc)

            return False

        self.loader.download(first_track)
        self.next_track_file = self.current_track_file = self.loader.get_track_path(first_track)
        self.station_info = {'id': station_id, 'name': name}
        Notify().info(f'Радиостанция "{name}" запущена')

        if is_immediately_play:
            self.play()

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

        scrobble = threading.Thread(name='Scrobble thread', target=self.scrobble, args=[self.track.id])
        scrobble.start()

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

    def repeate(self):
        self.player.stop()
        Notify().about_track(self.track, self.get_cover_path())
        self.player.play()

    def load_next_track(self):
        is_track_loaded = False
        self.next_track_file = None

        while is_track_loaded is False:
            if track := self.radio.play_next():
                is_track_loaded = self.loader.download(track)
            else:
                print('Can\'t get next track')
                sleep(1)

        self.next_track_file = self.loader.get_track_path(track)

    def next(self, callback=None):
        next_thread = threading.Thread(name='Start next track',
                                       target=self._next_as_background, args=[callback])
        next_thread.start()

    def scrobble(self, track_id):
        while self.get_current_playtime() < 30_000:
            sleep(1)

            if track_id != self.track.id:
                return

        self.lastfm.scrobble_track(self.track)

    def _next_as_background(self, callback):
        if is_locked('next'):
            Notify().info('Следующий трек уже загружается')
            return

        set_lock('next')
        self.track_history.append((self.track, self.loader.open_history_cover(self.track.id)))
        self.stop()

        wait_count = 0
        while self.next_track_file is None:
            print('Waiting next track %s sec' % wait_count)
            sleep(1)
            wait_count += 1

            if wait_count > 60:
                clear_lock('next')
                print('Can\'t await track')
                self.load_next_track()
                self._next_as_background(callback)
                exit(0)

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
        return self.loader.get_cover_path(self.track.id)

    def get_state(self):
        return str(self.player.get_state()).split('.')[1]

    def get_current_playtime(self):
        return int(self.player.get_time())

    def get_track_duration(self):
        return int(self.track.duration_ms)

    def get_history(self):
        return self.track_history

    def get_station(self):
        return self.station_info['name']

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
