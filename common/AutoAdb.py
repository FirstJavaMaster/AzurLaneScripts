# -*- coding: utf-8 -*-
import os
import subprocess

import cv2

import config


class AutoAdb:
    threshold = 0.9
    screen_pic_path = config.get(config.KEY_CACHE_DIR) + '/screen.png'

    def __init__(self):
        # 如果没有配置的话则从系统环境变量中获取
        adb_path = config.adb_path if config.adb_path else 'adb'
        try:
            subprocess.Popen([adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.adb_path = adb_path
            print('ADB PATH >>>> ' + self.adb_path, end='\n\n')

            # 初始化时验证设备连接情况
            self.test_device()
        except OSError:
            print('请配置ADB路径或将其配置到环境变量中')
            print('可参考下文中的相关说明: https://github.com/wangshub/wechat_jump_game/wiki')
            exit(1)

    def run(self, raw_command):
        command = '{} {}'.format(self.adb_path, raw_command)
        process = os.popen(command)
        output = process.read().strip()
        return output

    def test_device(self):
        print('检查设备是否连接...')
        command_list = [self.adb_path, 'devices']
        process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        lines = output[0].decode('utf8').splitlines()

        number = 0
        for each in lines:
            if each:
                print(each)
                number += 1
        if number != 2:
            print('找到 %s 个设备, 无法处理. 请保证只有一个设备存在' % (number - 1))
            exit(1)
        print('设备已连接', end='\n\n')
        self.test_screen()

        output = self.run('shell wm density')
        print("像素密度: " + output)
        output = self.run('shell getprop ro.product.device')
        print("系统类型: " + output)
        output = self.run('shell getprop ro.build.version.release')
        print('系统版本: ' + output)

    def test_screen(self):
        output = self.run('shell wm size')
        print('屏幕分辨率: ' + output)
        if 'Physical size: 1280x720' not in output:
            print('请将分辨率设置为 1280x720 (横向 平板模式)')
            exit(1)

    def screen_cap(self):
        self.run('exec-out screencap -p > ' + self.screen_pic_path)

    def get_location(self, temp_image_name, threshold=threshold):
        self.screen_cap()

        sp_gray = cv2.imread(self.screen_pic_path, cv2.COLOR_BGR2BGRA)
        temp_gray = cv2.imread(config.get(config.KEY_WORK_DIR) + '/temp_images/' + temp_image_name, cv2.COLOR_BGR2BGRA)

        res = cv2.matchTemplate(sp_gray, temp_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val < threshold:
            return None
        return max_loc

    def click(self, temp_image_name, threshold=threshold):
        loc = self.get_location(temp_image_name, threshold)
        if loc is None:
            return False

        img = cv2.imread(config.get(config.KEY_WORK_DIR) + '/temp_images/' + temp_image_name)
        h, w, _ = img.shape
        x = loc[0] + w / 2
        y = loc[1] + h / 2
        self.run('shell input tap %s %s' % (x, y))
        return True


if __name__ == '__main__':
    print('执行 main.py 启动脚本')
    exit(1)
