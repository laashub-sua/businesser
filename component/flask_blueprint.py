"""
auto registration the python module that under the rest folder python files
"""
import importlib
import os

rest_dir_name = 'rest'
ignore_dir_list = ['__pycache__']


def auto_registration_flask_blueprint(blueprint_path, module_name):
    from __init__ import app
    for item in os.listdir(blueprint_path):
        if item in ignore_dir_list:
            continue
        current_level_path = os.path.join(blueprint_path, item)
        cur_module_name = module_name + '.' + item
        if os.path.isdir(current_level_path):
            auto_registration_flask_blueprint(current_level_path, cur_module_name)
            continue
        cur_module_name = cur_module_name[:-3]
        target_dynamic_module = importlib.import_module(cur_module_name)
        if hasattr(target_dynamic_module, 'app'):
            app.register_blueprint(target_dynamic_module.app)


def do_init():
    auto_registration_flask_blueprint(rest_dir_name, rest_dir_name)
