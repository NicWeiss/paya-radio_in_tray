import base64
import glob
import os


class Loader:
    def __init__(self):
        self.assets_path = f'{os.path.dirname(os.path.realpath(__file__))}/../assets'
        self.file_path = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp'
        self.track_path = f'{self.file_path}/tracks'
        self.cover_path = f'{self.file_path}/covers'

        self._check_dirs()
        self._clear_data()

    def download(self, track):
        is_track_ready = self._download_track(track)
        self._download_cover(track)
        self._download_history_cover(track)

        return is_track_ready

    def get_track_path(self, track):
        return f'{self.track_path}/{track["id"]}.mp3'

    def open_cover(self, id):
        image_file = None

        try:
            image_file = open(f'{self.cover_path}/{id}.png', 'rb')
        except Exception:
            image_file = open(f'{self.assets_path}/default_cover.png', 'rb')

        return base64.b64encode(image_file.read()).decode('utf-8')

    def get_cover_path(self, id=None):
        try:
            image_path = f'{self.cover_path}/{id}_history.png'
            image_file = open(image_path, 'rb')
        except Exception:
            image_path = f'{self.assets_path}/default_cover.png'

        return image_path

    def open_history_cover(self, id):
        image_file = None

        try:
            image_file = open(f'{self.cover_path}/{id}_history.png', 'rb')
        except Exception:
            image_file = open(f'{self.assets_path}/default_cover.png', 'rb')

        return base64.b64encode(image_file.read()).decode('utf-8')

    def clear_data_by_id(self, id):
        track_file = f'{self.track_path}/{id}.mp3'
        cover_file = f'{self.cover_path}/{id}.png'
        history_cover_file = f'{self.cover_path}/{id}_history.png'

        try:
            os.remove(track_file)
            os.remove(cover_file)
            os.remove(history_cover_file)
        except Exception:
            pass

    def _check_dirs(self):
        if not os.path.isdir(self.track_path):
            os.makedirs(self.track_path)

        if not os.path.isdir(self.cover_path):
            os.makedirs(self.cover_path)

    def _clear_data(self):
        tracks = glob.glob(f'{self.track_path}/*')

        for track in tracks:
            if track in ['/', '..']:
                continue

            os.remove(track)

        covers = glob.glob(f'{self.cover_path}/*')

        for cover in covers:
            if cover in ['/', '..']:
                continue

            os.remove(cover)

    def _download_track(self, track):
        track_id = track['id']
        path_to_file = f'{self.track_path}/{track_id}.mp3'

        try:
            track.download(path_to_file)
        except Exception:
            return False

        print(f'[TRACK DOWNLOADED] {path_to_file}')

        return True

    def _download_cover(self, track):
        cover_id = track['id']
        path_to_file = f'{self.cover_path}/{cover_id}.png'
        try:
            track.download_cover(path_to_file, size='600x600')
        except Exception:
            return False

        print(f'[COVERDOWNLOADED] {path_to_file}')

    def _download_history_cover(self, track):
        cover_id = track['id']
        path_to_file = f'{self.cover_path}/{cover_id}_history.png'
        try:
            track.download_cover(path_to_file, size='100x100')
        except Exception:
            return False

        print(f'[COVERDOWNLOADED] {path_to_file}')
