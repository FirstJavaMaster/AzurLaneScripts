import os


def get_temp_rel_path_list(rel_dir):
    image_name_list = os.listdir(rel_dir)
    return [*map(lambda image_name: rel_dir + '/' + image_name, image_name_list)]
