import random

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

    def slider(self):
        print('滑动页面。 累积次数: %d.' % self.num)

        cursor_start = self.num % 4
        cursor_end = (self.num + 1) % 4

        pos_start = self.pos_list[cursor_start]
        pos_end = self.pos_list[cursor_end]
        self.auto_adb.swipe(*pos_start, *pos_end)

        # 每四次为一轮。从第二轮开始滑动会添加噪值
        if self.num < 4:
            return
        if 4 <= self.num < 8 or (self.num >= 8 and random.randint(0, 1) == 0):
            self.auto_adb.swipe(*pos_start, *pos_end)
