import json

from common import PathUtils


def init_config():
    print('配置初始化中...')
    work_dir = PathUtils.get_work_dir()
    print('脚本工作路径: ' + work_dir)
    cache_dir = PathUtils.get_cache_dir()
    print('缓存文件路径: ' + cache_dir)
    print()

    data = {
        'version': 0.1
    }

    with open(cache_dir + '/runtime.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


def get(key):
    with open(PathUtils.get_cache_dir() + '/runtime.json') as json_file:
        data = json.load(json_file)
        return data[key]
