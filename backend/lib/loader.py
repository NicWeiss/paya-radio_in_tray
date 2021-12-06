import base64
import glob
import os


class Loader:
    def __init__(self):
        self.file_path = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp'
        self.track_path = f'{self.file_path}/tracks'
        self.cover_path = f'{self.file_path}/covers'

        self._check_dirs()
        self._clear_data()

    def download(self, track):
        downloaded_track = self._download_track(track)
        self._download_cover(track)
        self._download_history_cover(track)

        return downloaded_track

    def open_cover(self, id):
        image_file = open(f'{self.cover_path}/{id}.png', 'rb')

        return base64.b64encode(image_file.read())

    def open_history_cover(self, id):
        image_file = open(f'{self.cover_path}/{id}_history.png', 'rb')

        return base64.b64encode(image_file.read())

    def clear_data_by_id(self, id):
        track_file = f'{self.track_path}/{id}.mp3'
        cover_file = f'{self.cover_path}/{id}.png'
        history_cover_file = f'{self.cover_path}/{id}_history.png'
        os.remove(track_file)
        os.remove(cover_file)
        os.remove(history_cover_file)

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
            if track in ['/', '..']:
                continue

            os.remove(cover)

    def _download_track(self, track):
        track_id = track['id']
        path_to_file = f'{self.track_path}/{track_id}.mp3'
        track.download(path_to_file)

        print(f'[TRACK DOWNLOADED] {path_to_file}')

        return path_to_file

    def _download_cover(self, track):
        cover_id = track['id']
        path_to_file = f'{self.cover_path}/{cover_id}.png'
        track.download_cover(path_to_file, size='600x600')

        print(f'[COVERDOWNLOADED] {path_to_file}')

    def _download_history_cover(self, track):
        cover_id = track['id']
        path_to_file = f'{self.cover_path}/{cover_id}_history.png'
        track.download_cover(path_to_file, size='100x100')

        print(f'[COVERDOWNLOADED] {path_to_file}')
