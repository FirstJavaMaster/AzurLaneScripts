# -*- coding: utf-8 -*-
import os
import subprocess
import time
from datetime import datetime

import cv2

import config
from common.Location import Location


class AutoAdb:
    threshold = 0.8
    wait_time = 1
    screen_pic_path = config.get_cache_dir() + '/screen.png'

    def __init__(self, test_device=False):
        self.adb_path = config.get_work_dir() + '/adb/adb.exe'
        if test_device:
            self.test_device()

    def run(self, raw_command):
        command = '{} {}'.format(self.adb_path, raw_command)
        process = os.popen(command)
        output = process.read().strip()
        return output

    def test_device(self):
        print('ADB PATH >>>> ' + self.adb_path, end='\n\n')
        try:
            subprocess.Popen([self.adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            print('ADB 配置有误')
            exit(1)

        print('检查设备 ...')
        command_list = [self.adb_path, 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        lines = output[0].decode('utf8').splitlines()

        device_number = -1  # -1 是为了去除"标题行"
        for line in lines:
            if line:
                print(line)
                device_number += 1
        if device_number < 1:
            print('未连接到设备, 请参考 https://github.com/FirstJavaMaster/AzurLaneScripts/blob/master/README.md')
            exit(1)
        if device_number > 2:
            print('设备数量过多, 请参考 https://github.com/FirstJavaMaster/AzurLaneScripts/blob/master/README.md')
            exit(1)
        print('设备已连接', end='\n\n')

        output = self.run('shell wm size')
        print('屏幕分辨率: ' + output)
        if 'Physical size: 1280x720' not in output:
            print('请将分辨率设置为 1280x720 (横向 平板模式)')
            exit(1)

        output = self.run('shell wm density')
        print("像素密度: " + output)
        output = self.run('shell getprop ro.product.device')
        print("系统类型: " + output)
        output = self.run('shell getprop ro.build.version.release')
        print('系统版本: ' + output)

    def screen_cap(self):
        self.run('exec-out screencap -p > ' + self.screen_pic_path)

    def get_location(self, *temp_rel_path_list, threshold=threshold):
        self.screen_cap()
        sp_gray = cv2.imread(self.screen_pic_path, cv2.COLOR_BGR2BGRA)

        for temp_rel_path in temp_rel_path_list:
            temp_abs_path = config.get_abs_path(temp_rel_path)
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

    def click(self, temp_rel_path, threshold=threshold):
        loc = self.get_location(temp_rel_path, threshold=threshold)
        if loc is None:
            return False
        return loc.click()

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        self.run('shell input swipe %d %d %d %d %d' % (start_x, start_y, end_x, end_y, duration))

    def wait(self, temp_rel_path, threshold=threshold, cycle_interval=0, max_wait_time=None, episode=None):
        start_time = datetime.now()
        while True:
            duration = (datetime.now() - start_time).seconds
            if max_wait_time is not None and 0 < max_wait_time < duration:
                print(' ×', flush=True)
                return Location(self, None, None, None)

            print('\r > wait %s ... %ds ' % (temp_rel_path, duration), end='')
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


if __name__ == '__main__':
    print('执行 main.py 启动脚本')
    exit(1)
