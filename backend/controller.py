import os.path
import threading
from time import sleep

import vlc

from backend.auth import Auth
from backend.player import Player
from backend.radio import Radio


class Controller():
    def __init__(self):
        self.auth = Auth()
        self.client = self.auth.auth_with_token()

        if self.client:
            self.start_radio(self.client)

    def start_radio(self, client):
        self.update_like_and_dislike_lists()
        self.radio = Radio(client)
        self.player = Player(self.radio)
        self.player.play()

        self.continious_play = threading.Thread(
            name='Continious playing', target=self.continious_play)
        self.continious_play.setDaemon(True)
        self.continious_play.start()

    def update_like_and_dislike_lists(self):
        self.liked_tracks = [track.id for track in self.client.users_likes_tracks()]
        self.disliked_tracks = [track.id for track in self.client.users_dislikes_tracks()]

    def continious_play(self):
        while True:
            sleep(1)

            try:
                if self.player.get_state() == 'Ended':
                    self.player.next()
            except Exception:
                return

    def actions(self, params):
        action = params['action']
        actions = {
            'logout': self.action_logout,
            'play': self.action_play,
            'pause': self.action_pause,
            'stop': self.action_stop,
            'next': self.action_next,
            'like': self.action_like,
            'dislike': self.action_dislike
        }

        if action == 'auth':
            credentials = params.get('user'), params.get('password')

            if client := self.auth.authentificate_from_credentials(*credentials):
                self.client = client
                self.start_radio(self.client)

                return self.get_client(None)
            else:
                return {'error': 'Can\'t authentificate, check user and password'}

        if not self.auth.is_authentificated:
            return {'error': 'Not authentificated!'}

        return actions[action](params)

    def action_logout(self, params):
        self.continious_play.signal = False
        self.continious_play = None
        self.client = None
        self.player.stop()
        self.player = None
        self.radio = None
        self.auth.logout()

    def action_play(self, params):
        self.player.play()

    def action_pause(self, params):
        self.player.pause()

    def action_stop(self, params):
        self.player.stop()

    def action_next(self, params):
        self.player.next()

    def action_like(self, params):
        track = self.player.get_track()
        self.client.users_likes_tracks_add(track.id)
        self.update_like_and_dislike_lists()

        return {'id': track.id, 'is_liked': True, 'is_disliked': False}

    def action_dislike(self, params):
        track = self.player.get_track()
        self.client.users_dislikes_tracks_add(track.id)
        self.update_like_and_dislike_lists()
        self.player.next()

        return {'id': track.id, 'is_liked': False, 'is_disliked': True}

    def getters(self, params):
        getter = params['get']
        getters = {
            'track': self.get_track,
            'player_state': self.get_player_state,
            'client': self.get_client
        }

        if not self.auth.is_authentificated:
            return {'error': 'Not authentificated!'}

        return getters[getter](params)

    def get_client(self, params):
        return {
            'token': self.client.token,
            'uid': self.client.me.account.uid,
            'login': self.client.me.account.login,
            'full_name': self.client.me.account.full_name,
            'display_name': self.client.me.account.display_name,
            'default_email': self.client.me.default_email
        }

    def get_track(self, params):
        track = self.player.get_track()

        return {
            'track': {
                'title': track.title,
                'artists': [artist.name for artist in track.artists],
                'is_liked': track.id in self.liked_tracks,
                'is_disliked': track.id in self.disliked_tracks,
            }
        }

    def get_player_state(self, params):
        return {
            'player_state': {
                'current_time': self.player.get_current_playtime(),
                'track_duration': self.player.get_track_duration(),
                'state': self.player.get_state()
            }
        }
