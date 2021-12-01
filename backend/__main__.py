import os.path
from time import sleep

import vlc
from yandex_music import Client

from player import Player
from radio import Radio


class YaRadio:
    def __init__(self):
        client = self.auth()
        radio = Radio(client)
        player = Player(radio)
        player.play()

        while True:
            sleep(1)

            if player.get_state() == vlc.State.Ended:
                player.next()


    def save_callback(self):
        print("Save Clicked")


    def auth(self):
        client = None
        token = None
        token_file_path = f'{os.path.dirname(os.path.realpath(__file__))}/tmp/token'
        # check token file

        if os.path.isfile(token_file_path):
            token_file = open('token', 'r')
            token = token_file.read()

        print(f'---------------------- Token is {token}')

        if token:
            print('---------------------- Auth by token')
            client = Client(token=token)
        else:
            print('---------------------- Auth by credentials')
            client = Client.from_credentials('dr.art.nic', '19377391Qq')
            token_file = open(token_file_path, 'w')
            token_file.write(client.token)
            token_file.close()

        return client


YaRadio()
