from common.AutoAdb import AutoAdb


class Slider:
    # 滑动次数
    num = 0
    # 增益。即连续同方向滑动次数。如果第一轮滑动还没找到敌人，则第二轮滑动中，每次滑动都会同方向滑动两次
    gain = 1
    # adb
    auto_adb = AutoAdb()

    pos_list = [
        [200, 200],  # 左上角
        [1100, 200],  # 右上角
        [1100, 600],  # 右下角
        [200, 600]  # 左下角
    ]

    def slider(self):
        print('滑动页面。 累积次数: %d. 滑动增益: %d.' % (self.num, self.gain))

        cursor_start = self.num % 4
        cursor_end = (self.num + 1) % 4

        pos_start = self.pos_list[cursor_start]
        pos_end = self.pos_list[cursor_end]

        for i in range(self.gain):
            self.auto_adb.swipe(*pos_start, *pos_end)

        self.gain = self.num // 4 + 1
