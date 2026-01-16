import configparser
import os

_config = None  # Global cache


def read_config():
    global _config
    if _config is None:
        _config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), '..', 'Config_Files', 'config.ini')
        _config.read(config_path)
    return _config


def get_browser():
    config = read_config()
    return config['settings']['browser']


def get_url():
    config = read_config()
    return config['settings']['url']
