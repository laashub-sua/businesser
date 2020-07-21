import os

import yaml


def load(config_file_path):
    if not os.path.exists(config_file_path):
        raise Exception("config file not exists")
    with open(config_file_path) as f:
        return yaml.safe_load(f.read())
