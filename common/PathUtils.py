import os


# 获取项目路径
def get_work_dir():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(curr_dir)


# 获取项目的缓存路径
def get_cache_dir():
    cache_dir = get_work_dir() + '/cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        return cache_dir
    if not os.path.isdir(cache_dir):
        os.remove(cache_dir)
        os.makedirs(cache_dir)
        return cache_dir
    return cache_dir


# 根据相对路径生成绝对路径
def get_abs_path(*rel_paths):
    return os.path.join(get_work_dir(), *rel_paths)
