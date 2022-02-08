import threading
from time import sleep

import vlc

from backend.lib.loader import Loader


class Player():
    def __init__(self, radio, station):
        self.is_waiting = False
        self.next_track_file = None
        self.radio = radio
        self.player = vlc.MediaPlayer()
        self.loader = Loader()
        self.track_history = []

        first_track = radio.start_radio(station, '')
        self.loader.download(first_track)
        self.current_track_file = self.loader.get_track_path(first_track)

    def play(self):
        if self.get_state() == 'Playing':
            return True

        if self.get_state() == 'Paused':
            return self.pause()

        self.track = self.radio.get_current_track()
        track_title = self.track['title']
        artist_name = self.track['artists'][0]['name']

        media = vlc.Media(f'file://{self.current_track_file}')
        self.player.set_media(media)
        self.player.play()

        print(f'[Playing] {artist_name}: {track_title}')

        self.next_track_file = None
        download = threading.Thread(name='Continious playing', target=self.load_next_track)
        download.setDaemon(True)
        download.start()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def load_next_track(self):
        track = self.radio.play_next()
        self.next_track_file = None

        # todo: положить в цикл, выполнять до тех пор пока не загрузится корректный трек
        self.loader.download(track)
        self.next_track_file = self.loader.get_track_path(track)

    def next(self):
        self.is_waiting = True
        self.track_history.append((self.track, self.loader.open_history_cover(self.track.id)))
        self.stop()
        self.loader.clear_data_by_id(self.track.id)

        while self.next_track_file == None:
            print('Waiting next track')
            sleep(1)

        self.is_waiting = False
        self.current_track_file = self.next_track_file
        self.play()

    def get_track(self):
        return self.track

    def get_cover(self):
        return self.loader.open_cover(self.track.id)

    def get_state(self):
        return str(self.player.get_state()).split('.')[1]

    def get_current_playtime(self):
        return int(self.player.get_time())

    def get_track_duration(self):
        return int(self.track.duration_ms)

    def get_history(self):
        return self.track_history
