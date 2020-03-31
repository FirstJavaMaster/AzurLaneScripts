import os


# 获取项目路径
def get_work_dir():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(curr_dir)


# 获取项目的缓存路径
def get_cache_dir():
    cache_dir = get_work_dir() + '/cache'
    mkdir_ensure(cache_dir)
    return cache_dir


# 根据相对路径获取绝对路径
def get_abs_path(*rel_paths):
    return os.path.join(get_work_dir(), *rel_paths)


# 创建文件夹。确保能创建成功
def mkdir_ensure(dir_target):
    if os.path.isdir(dir_target):
        return False

    if os.path.isfile(dir_target):
        os.remove(dir_target)
    os.makedirs(dir_target)
    return True


# 创建文件。确保能创建成功
def touch_ensure(file_target):
    if os.path.isfile(file_target):
        return False

    if os.path.isdir(file_target):
        os.removedirs(file_target)
    os.mknod(file_target)
    return True
