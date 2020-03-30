from common.AutoAdb import AutoAdb


# 判断船坞是否满员
def check_port_full():
    auto_adb = AutoAdb()
    port_full = auto_adb.check('temp_images/port-full.png')
    if port_full:
        print('船坞已经满员了, 请整理')
        exit(1)
