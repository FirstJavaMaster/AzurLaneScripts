import json
import os

# 用户自定义配置区域
adb_path = r'D:\AndroidSDK\platform-tools\adb.exe'


###

###

# 方法区

# 获取项目路径
def get_work_dir():
    return os.path.dirname(os.path.abspath(__file__))


# 获取项目的缓存路径
def get_cache_dir():
    return get_work_dir() + '/cache'


# 根据相对路径生成绝对路径
def get_abs_path(*rel_paths):
    return os.path.join(get_work_dir(), *rel_paths)


def init_config():
    print('配置初始化中...')
    work_dir = get_work_dir()
    print('脚本工作路径: ' + work_dir)
    cache_dir = get_cache_dir()
    print('缓存文件路径: ' + cache_dir)
    print()

    data = {
        'version': 0.1
    }

    with open(cache_dir + '/runtime.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


def get(key):
    with open(get_cache_dir() + '/runtime.json') as json_file:
        data = json.load(json_file)
        return data[key]
