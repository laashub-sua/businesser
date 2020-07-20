"""
load project's properties yaml file to python dict for use simple
"""
import os

import yaml

project_root_path = os.getcwd()
project_config_dir = os.path.join("configs")


def load():
    data = {}
    for item in os.listdir(project_config_dir):
        project_config_file_name = item[:-4]
        with open(os.path.join(project_config_dir, item)) as f:
            data[str(project_config_file_name)] = yaml.safe_load(f.read())
    return data
