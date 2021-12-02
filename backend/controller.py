import os.path
import threading
from time import sleep

import vlc
from yandex_music import Client

from backend.player import Player
from backend.radio import Radio


class Controller():
    def __init__(self):
        client = self.auth()
        self.liked_tracks = [track.id for track in client.users_likes_tracks()]
        self.disliked_tracks = [track.id for track in client.users_dislikes_tracks()]
        radio = Radio(client)
        self.player = Player(radio)
        self.player.play()

        continious_play = threading.Thread(name='Continious playing', target=self.continious_play)
        continious_play.setDaemon(True)
        continious_play.start()

    def actions(self, action):
        if action == 'play':
            self.player.play()
        elif action == 'pause':
            self.player.pause()
        elif action == 'stop':
            self.player.stop()
        elif action == 'next':
            self.player.next()

    def getters(self, getter):
        if getter == 'track':
            track = self.player.get_track()
            return {
                "track": track,
                "is_liked": track.id in self.liked_tracks,
                "is_disliked": track.id in self.disliked_tracks,
            }

    def continious_play(self):
        while True:
            sleep(1)

            if self.player.get_state() == vlc.State.Ended:
                self.player.next()

    def auth(self):
        client = None
        token = None
        token_file_path = f'{os.path.dirname(os.path.realpath(__file__))}/tmp/token'

        if os.path.isfile(token_file_path):
            token_file = open(token_file_path, 'r')
            token = token_file.read()

        if token:
            print('---------------------- Auth by token ----------------------')
            client = Client(token=token)
        else:
            print('---------------------- Auth by credentials ----------------------')
            client = Client.from_credentials('dr.art.nic', '19377391Qq')
            token_file = open(token_file_path, 'w')
            token_file.write(client.token)
            token_file.close()

        return client
