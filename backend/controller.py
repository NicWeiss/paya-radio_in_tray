import threading
from time import sleep

from backend.lib.auth import Auth
from backend.lib.helpers import check_auth
from backend.lib.radio import Radio
from backend.lib.router import url
from backend.player import Player


class Controller():
    test = 'sccss'

    def __init__(self):
        self.auth = Auth()
        self.client = self.auth.auth_with_token()

        if self.client:
            self.start_radio(self.client)

    def start_radio(self, client):
        self.update_like_and_dislike_lists()
        self.radio = Radio(client)
        self.player = Player(self.radio, 'user:onyourwave')
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

    @url('/api/auth')
    def actions(self, params):
        credentials = params.get('user'), params.get('password')

        if client := self.auth.authentificate_from_credentials(*credentials):
            self.client = client
            self.start_radio(self.client)

            return self.get_client(None)
        else:
            return {'error': 'Can\'t authentificate, check user and password'}

    @check_auth
    @url('/api/logout')
    def action_logout(self, params):
        self.continious_play.signal = False
        self.continious_play = None
        self.client = None
        self.player.stop()
        self.player = None
        self.radio = None
        self.auth.logout()

    @check_auth
    @url('/api/play')
    def action_play(self, params):
        self.player.play()

    @check_auth
    @url('/api/pause')
    def action_pause(self, params):
        self.player.pause()

    @check_auth
    @url('/api/stop')
    def action_stop(self, params):
        self.player.stop()

    @check_auth
    @url('/api/next')
    def action_next(self, params):
        self.player.next()

    @check_auth
    @url('/api/like')
    def action_like(self, params):
        track = self.player.get_track()
        self.client.users_likes_tracks_add(track.id)
        self.update_like_and_dislike_lists()

        return {'id': track.id, 'is_liked': True, 'is_disliked': False}

    @check_auth
    @url('/api/dislike')
    def action_dislike(self, params):
        track = self.player.get_track()
        self.client.users_dislikes_tracks_add(track.id)
        self.update_like_and_dislike_lists()
        self.player.next()

        return {'id': track.id, 'is_liked': False, 'is_disliked': True}

    @check_auth
    @url('/api/client')
    def get_client(self, params):
        return {
            'token': self.client.token,
            'uid': self.client.me.account.uid,
            'login': self.client.me.account.login,
            'full_name': self.client.me.account.full_name,
            'display_name': self.client.me.account.display_name,
            'default_email': self.client.me.default_email
        }

    @check_auth
    @url('/api/player_state')
    def get_player_state(self, params):
        return {
            'player_state': {
                'playing_track_id': self.player.get_track().id,
                'current_time': self.player.get_current_playtime(),
                'track_duration': self.player.get_track_duration(),
                'state': self.player.get_state()
            }
        }

    @check_auth
    @url('/api/track')
    def get_track(self, params):
        track = self.player.get_track()
        cover = self.player.get_cover()

        return {'track': self.build_track(track, cover)}

    @check_auth
    @url('/api/history')
    def get_history(self, params):
        history = self.player.get_history()
        jsonified_history = {'history': []}

        # import pdb
        # pdb.set_trace()

        for track, cover in history:
            jsonified_history['history'].append(self.build_track(track, cover))

        return jsonified_history

    def build_track(self, track, cover):
        return {
            'id': track.id,
            'title': track.title,
            'artists': [artist.name for artist in track.artists],
            'is_liked': track.id in self.liked_tracks,
            'is_disliked': track.id in self.disliked_tracks,
            'cover': cover
        }
