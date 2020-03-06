import json
import os

# 用户自定义配置区域
adb_path = r'D:\AndroidSDK\platform-tools\adb.exe'

###

# 常量区域
KEY_WORK_DIR = 'work_dir'
KEY_CACHE_DIR = 'cache_dir'


###

# 方法区
def __init_file__():
    print('配置初始化中...')
    work_dir = os.getcwd()
    print('脚本工作路径: ' + work_dir)
    cache_dir = os.path.join(work_dir, 'cache')
    print('缓存文件路径: ' + cache_dir)
    print()

    data = {
        KEY_WORK_DIR: work_dir,
        KEY_CACHE_DIR: cache_dir
    }

    with open('cache/runtime.json', 'w') as json_file:
        json.dump(data, json_file)


def get(key):
    with open('cache/runtime.json') as json_file:
        data = json.load(json_file)
        return data[key]
