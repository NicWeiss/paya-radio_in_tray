import os

import eyed3
from eyed3.id3.frames import ImageFrame
from os import walk

FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/../tmp'
TRACK_PATH = f'{FILE_PATH}/export'


def export_user_playlists(client):
    plsts = client.users_playlists_list()
    failed = []

    for pl in plsts:
        tracks = pl.fetch_tracks()

        for obj in tracks:
            track = obj.track
            name = f"{track['artists'][0]['name']} - {track['title']}.mp3".replace("/", ' ').replace('"', "'").replace("?", "").replace(":", " ")
            path_to_file = f'{TRACK_PATH}/{name}'

            filenames = next(walk(TRACK_PATH), (None, None, []))[2]
            if name in filenames:
                print(f'[TRACK EXIST] {path_to_file}')
                continue

            if track.available is False:
                failed.append(name)
                print(f'[TRACK IS NOT AVAILABLE] {path_to_file}')
                continue

            is_exported, track_name = export_track(track)
            if not is_exported:
                failed.append(track_name)

    print('[NEXT TRACKS IS NO MORE AVAILABLE]:')
    with open(f"{TRACK_PATH}/list_unavalable_tracks.txt", "w", encoding='utf-8') as f:
        for fail in list(set(failed)):
            print(fail.replace(".mp3", ""))
            f.write(fail.replace(".mp3", "") + '\n')


def export_track(track):
    name = f"{track['artists'][0]['name']} - {track['title']}.mp3".replace("/", ' ').replace('"', "'")
    path_to_file = f'{TRACK_PATH}/{name}'

    isNotLoaded = True
    max_try = 0

    while isNotLoaded:
        try:
            track.download(path_to_file)
            isNotLoaded = False
        except Exception as exc:
            print(f'/ CAN\'T LOAD FILE / {path_to_file}: {str(exc)}')
            breakpoint()
            max_try += 1

        if max_try > 3:
            isNotLoaded = False

    if max_try > 3:
        return False, name

    try:
        path_to_cover = f'{TRACK_PATH}/cover.png'
        url = f'https://{track.__dict__["albums"][0]["cover_uri"][:-3]}/600x600'
        track.client.request.download(url, path_to_cover)

        audiofile = eyed3.load(path_to_file)
        if (audiofile.tag is None):
            audiofile.initTag()

        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(path_to_cover,'rb').read(), 'image/png')

        audiofile.tag.save()
        os.remove(path_to_cover)
    except Exception as exc:
        print(f'/ CAN\'T ADD COVER TO FILE / {path_to_file}: {str(exc)}')
        return True, name

    print(f'[TRACK EXPORTED] {path_to_file}')
    return True, name
