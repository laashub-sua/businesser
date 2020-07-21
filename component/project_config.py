"""
load project's properties yaml file to python dict for use simple
"""
import os

from component import configer

project_root_path = os.getcwd()
project_config_dir = os.path.join("configs")


def load():
    data = {}
    for item in os.listdir(project_config_dir):
        project_config_file_name = item[:-4]
        data[str(project_config_file_name)] = configer.load(os.path.join(project_config_dir, item))
    return data
