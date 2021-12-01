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
        if self.player.get_state() == vlc.State.Playing:
            return True

        self.track = self.radio.get_current_track()
        media = vlc.Media(f'file://{self.current_track_file}')
        self.player.set_media(media)
        self.player.play()
        print('Playing')

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

        os.remove(self.current_track_file)
        self.current_track_file = self.next_track_file
        self.play()

    def get_state(self):
        return self.player.get_state()

    def _download(self, track, is_next=False):
        if is_next:
            self.next_track_file = None

        track_id = track['id']
        track_title = track['title']
        files = '/tmp/yaradio/'

        if not os.path.isdir(files):
            os.makedirs(files)

        path_to_file = f'/tmp/yaradio/{track_id}.mp3'
        track.download(path_to_file)
        print(f'{track_title} - downloaded')

        if is_next:
            self.next_track_file = path_to_file
        else:
            return path_to_file
