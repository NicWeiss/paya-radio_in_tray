import threading
from time import sleep

from backend.lib.auth import Auth
from backend.lib.headphones import HeadphonesObserver
from backend.lib.helpers import check_auth
from backend.lib.notify import Notify
from backend.lib.radio import Radio
from backend.lib.router import url
from backend.lib.tray_menu import TrayMenu
from backend.player import Player


class Controller():

    def __init__(self, config):
        self.config = config
        self.auth = Auth(config)
        self.client = self.auth.auth_with_token()

        if self.client:
            self.start_tray()
            self.start_radio(self.client)

    def start_tray(self):
        stations_list = self.client.rotor_stations_list()
        recomended_station_list = self.client.rotor_stations_dashboard()

        self.stations = {'all': {}, 'all': {}}

        for station in stations_list:
            station_object = {
                "name": station["station"]["name"],
                "id": f'{station["station"]["id"]["type"]}:{station["station"]["id"]["tag"]}'
            }

            if self.stations['all'].get(station["station"]["id"]["type"]) is None:
                self.stations['all'][station["station"]["id"]["type"]] = []

            self.stations['all'][station["station"]["id"]["type"]].append(station_object)

        self.stations['rec'] = [{
            "name": station["station"]["name"],
            "id": f'{station["station"]["id"]["type"]}:{station["station"]["id"]["tag"]}'
        } for station in recomended_station_list['stations']]

        self.tray_menu = TrayMenu(self.config, self.action_like, self.action_dislike, self.stations)

    def start_radio(self, client):
        self.radio = Radio(client)
        self.player = Player(self.radio, self.config['backend']['default_station'])
        self.update_like_and_dislike_lists()
        self.tray_menu.set_player(self.player)
        HeadphonesObserver(self.player)
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
    def action_auth(self, query_params=None):
        credentials = query_params.get('user'), query_params.get('password')

        if client := self.auth.authentificate_from_credentials(*credentials):
            self.client = client
            self.start_radio(self.client)

            return self.get_client(None)
        else:
            return {'error': 'Can\'t authentificate, check user and password'}

    @check_auth
    @url('/api/logout')
    def action_logout(self, query_params=None):
        self.continious_play.signal = False
        self.continious_play = None
        self.client = None
        self.player.stop()
        self.player = None
        self.radio = None
        self.auth.logout()

    @check_auth
    @url('/api/play')
    def action_play(self, query_params=None):
        self.player.play()

    @check_auth
    @url('/api/pause')
    def action_pause(self, query_params=None):
        self.player.pause()

    @check_auth
    @url('/api/stop')
    def action_stop(self, query_params=None):
        self.player.stop()

    @check_auth
    @url('/api/next')
    def action_next(self, query_params=None):
        self.player.next()

    @check_auth
    @url('/api/like')
    def action_like(self, query_params=None):
        if not self.player:
            return

        track = self.player.get_track()
        self.client.users_likes_tracks_add(track.id)
        self.update_like_and_dislike_lists()

        return {'id': track.id, 'is_liked': True, 'is_disliked': False}

    @check_auth
    @url('/api/dislike')
    def action_dislike(self, query_params=None):
        if not self.player:
            return

        self.player.stop()
        track = self.player.get_track()
        self.client.users_dislikes_tracks_add(track.id)
        self.update_like_and_dislike_lists()
        self.player.next()

        return {'id': track.id, 'is_liked': False, 'is_disliked': True}

    @check_auth
    @url('/api/client')
    def get_client(self, query_params=None):
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
    def get_player_state(self, query_params=None):
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
    def get_track(self, query_params=None):
        track = self.player.get_track()
        cover = self.player.get_cover()

        return {'track': self.build_track(track, cover)}

    @check_auth
    @url('/api/history')
    def get_history(self, query_params=None):
        history = self.player.get_history()
        jsonified_history = {'history': []}

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
