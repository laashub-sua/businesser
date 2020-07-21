import os


def find_third_party_path(cur_dir_path=None, path_tag='third_party'):
    return find_tag_path(path_tag, cur_dir_path)


def find_tag_path(path_tag, cur_dir_path=None):
    if not cur_dir_path:
        cur_dir_path = os.getcwd()
    if not os.path.exists(cur_dir_path):
        raise Exception('the target find path is not exists')
    if path_tag in os.listdir(cur_dir_path):
        return os.path.join(cur_dir_path, path_tag)
    else:
        return find_tag_path(path_tag, cur_dir_path[:cur_dir_path.rfind('\\')])
