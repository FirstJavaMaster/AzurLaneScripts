# 记录位置信息的类
import time


class Location:
    auto_adb = None
    temp_abs_path = None
    pos_x = None
    pos_y = None

    # 默认等待时间
    wait_time = 1

    def __init__(self, auto_adb, temp_abs_path, pos_x, pos_y):
        self.auto_adb = auto_adb
        self.temp_abs_path = temp_abs_path
        self.pos_x = pos_x
        self.pos_y = pos_y

    def click(self, wait_time=wait_time):
        if self.pos_x is None:
            return False

        self.auto_adb.run('shell input tap %s %s' % (self.pos_x, self.pos_y))
        print('click [√] ' + self.temp_abs_path)
        time.sleep(wait_time)
        return True


if __name__ == '__main__':
    print('执行 main.py 启动脚本')
    exit(1)
