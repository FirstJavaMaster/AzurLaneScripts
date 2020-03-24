from configparser import ConfigParser

from common import PathUtils


def get(key, section='default', fallback=None):
    cp = ConfigParser()
    cp.read(PathUtils.get_work_dir() + '/config.ini')
    return cp.get(section, key, fallback=fallback)
