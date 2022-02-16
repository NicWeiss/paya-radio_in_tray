import os

import yaml


class ConfigUtils():

    def get_config(self, section=None):
        with open(os.path.dirname(__file__) + '/../../config/config.yaml', 'r') as ymlfile:
            config = yaml.load(ymlfile)
        return config[section] if section else config
