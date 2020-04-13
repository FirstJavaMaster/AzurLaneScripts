# -*- coding: utf-8 -*-
import os
import time

import cv2

from common import PathUtils, AutoAdbCheck, ConfigUtils
from common.Location import Location
from common.Timer import Timer


class AutoAdb:
    threshold = 0.8
    wait_time = 1
    screen_pic_path = PathUtils.get_cache_dir() + '/screen.png'

    def __init__(self, test_device=False):
        self.adb_path = PathUtils.get_work_dir() + '/adb/adb.exe'
        if test_device:
            AutoAdbCheck.test_device(self)

    def run(self, raw_command):
        adb_host_port = ConfigUtils.get('adb_host_port')
        command = '%s -s %s %s' % (self.adb_path, adb_host_port, raw_command)
        res = os.popen(command)
        return res.buffer.read().decode('utf-8').strip()

    def screen_cap(self):
        self.run('exec-out screencap -p > ' + self.screen_pic_path)

    def get_location(self, *temp_rel_path_list, threshold=threshold):
        self.screen_cap()
        sp_gray = cv2.imread(self.screen_pic_path, cv2.COLOR_BGR2BGRA)

        for temp_rel_path in temp_rel_path_list:
            temp_abs_path = PathUtils.get_abs_path(temp_rel_path)
            temp_gray = cv2.imread(temp_abs_path, cv2.COLOR_BGR2BGRA)

            res = cv2.matchTemplate(sp_gray, temp_gray, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if max_val < threshold:
                continue

            h, w, _ = cv2.imread(temp_abs_path).shape
            x = max_loc[0] + w / 2
            y = max_loc[1] + h / 2
            return Location(self, temp_rel_path, x, y)
        return None

    def check(self, temp_rel_path):
        loc = self.get_location(temp_rel_path)
        return loc is not None

    def click(self, temp_rel_path, threshold=threshold, wait_time=wait_time):
        loc = self.get_location(temp_rel_path, threshold=threshold)
        if loc is None:
            return False
        return loc.click(wait_time)

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        self.run('shell input swipe %d %d %d %d %d' % (start_x, start_y, end_x, end_y, duration))

    def wait(self, temp_rel_path, threshold=threshold, cycle_interval=0, max_wait_time=None, episode=None):
        timer = Timer()
        while True:
            duration = timer.get_duration()
            print('\r > wait %s ... %ds ' % (temp_rel_path, duration), end='')

            if max_wait_time is not None and 0 < max_wait_time < duration:
                print(' ×', flush=True)
                return Location(self, None, None, None)

            if episode is not None:
                try:
                    episode()
                except Exception as e:
                    print('过程方法执行异常')
                    print(e)

            loc = self.get_location(temp_rel_path, threshold=threshold)
            if loc is not None:
                print(' √', flush=True)
                return loc

            if cycle_interval > 0:
                time.sleep(cycle_interval)
