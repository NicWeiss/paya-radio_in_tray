import os
import threading

import vlc


class Player():
    def __init__(self, radio):
        self.next_track_file = None
        self.radio = radio
        self.player = vlc.MediaPlayer()

        track = radio.start_radio('user:onyourwave', '')
        self.current_track_file = self._download(track)

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

        download = threading.Thread(name='Continious playing',
                                    target=self._download,
                                    args=(self.radio.play_next(), True))
        download.setDaemon(True)
        download.start()

    def get_track(self):
        return self.track

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        if not self.next_track_file:
            return False

        self.stop()
        os.remove(self.current_track_file)
        self.current_track_file = self.next_track_file
        self.play()

    def get_state(self):
        return str(self.player.get_state()).split('.')[1]

    def get_current_playtime(self):
        return int(self.player.get_time())

    def get_track_duration(self):
        return int(self.track.duration_ms)

    def _download(self, track, is_next=False):
        if is_next:
            self.next_track_file = None

        track_id = track['id']
        files = '/tmp/yaradio/'

        if not os.path.isdir(files):
            os.makedirs(files)

        path_to_file = f'/tmp/yaradio/{track_id}.mp3'
        track.download(path_to_file)
        print(f'[DOWNLOADED] {path_to_file}')

        if is_next:
            self.next_track_file = path_to_file
        else:
            return path_to_file
