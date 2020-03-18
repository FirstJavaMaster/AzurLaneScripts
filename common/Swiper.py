from common.AutoAdb import AutoAdb

pos_1 = [200, 200]
pos_2 = [1100, 200]
pos_3 = [1100, 600]
pos_4 = [200, 600]


def swipe(num):
    flag = num % 4

    if flag == 1:
        pos_start = pos_1
        pos_end = pos_2
    elif flag == 2:
        pos_start = pos_2
        pos_end = pos_3
    elif flag == 3:
        pos_start = pos_3
        pos_end = pos_4
    else:
        pos_start = pos_4
        pos_end = pos_1

    auto_adb = AutoAdb()
    auto_adb.swipe(*pos_start, *pos_end)
