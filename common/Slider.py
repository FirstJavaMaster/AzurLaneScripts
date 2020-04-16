import random
import time

from common.AutoAdb import AutoAdb


class Slider:
    # 滑动次数
    num = 0
    # adb
    auto_adb = AutoAdb()

    pos_list = [
        [200, 200],  # 左上角
        [1100, 200],  # 右上角
        [1100, 600],  # 右下角
        [200, 600]  # 左下角
    ]

    def slide(self):
        print('滑动页面。 累积次数: %d.' % self.num)

        cursor_start = self.num % 4
        cursor_end = (self.num + 1) % 4

        pos_start = self.pos_list[cursor_start]
        pos_end = self.pos_list[cursor_end]
        self.auto_adb.swipe(*pos_start, *pos_end)

        # 每四次为一轮。从第二轮开始滑动会添加噪值
        if 4 <= self.num < 8 or (self.num >= 8 and random.randint(0, 1) == 0):
            self.auto_adb.swipe(*pos_start, *pos_end)
        # +1
        self.num += 1

        # 滑动完毕后等待，有时动画导致敌人无法判断
        time.sleep(1)

    # 单向滑动
    # direction 滑动方向，1、2、3、4分别代表上下左右
    # num 滑动 次数
    def slide_unidirectional(self, direction, num=1):
        if num is None or num <= 0:
            return

        if direction == 1:
            pos_start = self.pos_list[0]
            pos_end = self.pos_list[3]
        elif direction == 2:
            pos_start = self.pos_list[3]
            pos_end = self.pos_list[0]
        elif direction == 3:
            pos_start = self.pos_list[1]
            pos_end = self.pos_list[0]
        else:
            pos_start = self.pos_list[0]
            pos_end = self.pos_list[1]

        while True:
            if num == 0:
                break
            self.auto_adb.swipe(*pos_start, *pos_end)
            num -= 1
