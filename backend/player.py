import os
import pdb
from time import sleep

import vlc


class Player():
    def __init__(self, radio):
        self.radio = radio
        self.player = vlc.MediaPlayer()

        track = radio.start_radio('user:onyourwave', '')
        self.current_track = self._download(track)

    def play(self):
        if self.player.get_state() == vlc.State.Playing:
            return True

        media = vlc.Media(f'file://{self.current_track}')
        self.player.set_media(media)
        self.player.play()
        print('Playing')

        self.next_track = self._download(self.radio.play_next())

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def next(self):
        os.remove(self.current_track)
        self.current_track = self.next_track
        self.play()

    def get_state(self):
        return self.player.get_state()

    def _download(self, track):
        track_id = track['id']
        track_title = track['title']

        path_to_file = f'/tmp/yaradio/{track_id}.mp3'
        track.download(path_to_file)
        print(f'{track_title} - downloaded')

        return path_to_file
