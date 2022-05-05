import base64
import glob
import json
import os
from backend.lib.jsonify import jsonify

from yandex_music import Track, Artist


SAVED_TRACK_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp/saved_track'
ASSETS_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/../assets'
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp'
TRACK_PATH = f'{FILE_PATH}/tracks'
COVER_PATH = f'{FILE_PATH}/covers'


class Loader:
    def __init__(self):
        self._check_dirs()
        self._clear_data()

    def store_track(self, track):
        artists_to_store = []

        for artist in track.artists:
            artist_to_store = {
                'id': artist.id,
                'name': artist.name
            }

            artists_to_store.append(artist_to_store)

        track_to_store = {
            'id': track.id,
            'id_': track.id,
            'title': track.title,
            'duration_ms': track.duration_ms,
            'cover_uri': track.cover_uri,
            'artists': artists_to_store
        }
        current_track_file = open(SAVED_TRACK_PATH, 'w')
        current_track_file.write(jsonify(track_to_store).decode())
        current_track_file.close()

    def load_saved_track(self):
        try:
            last_track_file = open(SAVED_TRACK_PATH, 'r')
        except Exception:
            return {}

        return json.loads(last_track_file.read())

    def restore_track(self, client):
        if track_dict := self.load_saved_track():
            restored_artists = [Artist(art['id'], name=art['name'])
                                for art in track_dict.pop('artists')]
            restored_track = Track(**track_dict, artists=restored_artists, client=client)

            return restored_track
        else:
            return None

    def download(self, track):
        is_track_ready = self._download_track(track)
        self._download_cover(track)
        self._download_history_cover(track)

        return is_track_ready

    def get_track_path(self, track):
        return f'{TRACK_PATH}/{track["id"]}.mp3'

    def open_cover(self, id):
        image_file = None

        try:
            image_file = open(f'{COVER_PATH}/{id}.png', 'rb')
        except Exception:
            image_file = open(f'{ASSETS_PATH}/default_cover.png', 'rb')

        return base64.b64encode(image_file.read()).decode('utf-8')

    def get_cover_path(self, id=None):
        try:
            image_path = f'{COVER_PATH}/{id}_history.png'
            image_file = open(image_path, 'rb')
        except Exception:
            image_path = f'{ASSETS_PATH}/default_cover.png'

        return image_path

    def open_history_cover(self, id):
        image_file = None

        try:
            image_file = open(f'{COVER_PATH}/{id}_history.png', 'rb')
        except Exception:
            image_file = open(f'{ASSETS_PATH}/default_cover.png', 'rb')

        return base64.b64encode(image_file.read()).decode('utf-8')

    def clear_data_by_id(self, id):
        track_file = f'{TRACK_PATH}/{id}.mp3'
        cover_file = f'{COVER_PATH}/{id}.png'
        history_cover_file = f'{COVER_PATH}/{id}_history.png'

        try:
            os.remove(track_file)
            os.remove(cover_file)
            os.remove(history_cover_file)
        except Exception:
            pass

    def _check_dirs(self):
        if not os.path.isdir(TRACK_PATH):
            os.makedirs(TRACK_PATH)

        if not os.path.isdir(COVER_PATH):
            os.makedirs(COVER_PATH)

    def _clear_data(self):
        tracks = glob.glob(f'{TRACK_PATH}/*')
        saved_id = None

        if saved_track := self.load_saved_track():
            saved_id = saved_track.get('id')

        for track in tracks:
            if track.split('/')[-1] in ['/', '..', f'{saved_id}.mp3']:
                continue

            os.remove(track)

        covers = glob.glob(f'{COVER_PATH}/*')

        for cover in covers:
            if cover.split('/')[-1] in ['/', '..', f'{saved_id}.png', f'{saved_id}_history.png']:
                continue

            os.remove(cover)

    def _download_track(self, track):
        track_id = track['id']
        path_to_file = f'{TRACK_PATH}/{track_id}.mp3'

        try:
            track.download(path_to_file)
        except Exception:
            return False

        print(f'[TRACK DOWNLOADED] {path_to_file}')

        return True

    def _download_cover(self, track):
        cover_id = track['id']
        path_to_file = f'{COVER_PATH}/{cover_id}.png'
        try:
            track.download_cover(path_to_file, size='600x600')
        except Exception:
            return False

        print(f'[COVERDOWNLOADED] {path_to_file}')

    def _download_history_cover(self, track):

        if not track:
            return

        cover_id = track['id']
        path_to_file = f'{COVER_PATH}/{cover_id}_history.png'

        try:
            track.download_cover(path_to_file, size='100x100')
        except Exception:
            return False

        print(f'[COVERDOWNLOADED] {path_to_file}')
