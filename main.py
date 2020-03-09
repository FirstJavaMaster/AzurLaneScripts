import os
import time

import config
from common.AutoAdb import AutoAdb


def run():
    # 首先到主界面
    go_to_main_page()

    auto_adb = AutoAdb()
    # 主界面出击
    auto_adb.click('temp_images/main-fight.png')
    # 选择关卡
    pick_round()

    # 判断船坞是否满员
    port_full = auto_adb.check('temp_images/port-full.png')
    if port_full:
        print('船坞已经满员了, 请整理')
        auto_adb.click('temp_images/port-full-arrange.png')
        exit(1)

    while True:
        # 寻找敌人
        res = provoke_enemy(auto_adb)
        if not res:
            exit(1)

        # 处理自律战斗的提示
        res = auto_adb.click_finally('temp_images/auto-fight-confirm-1.png', max_wait_time=3)
        if res:
            print('确认自动战斗')
            auto_adb.click_finally('temp_images/auto-fight-confirm-2.png')

        # 找到敌人后开始出击
        auto_adb.click_finally('temp_images/fight.png')

        print('战斗开始 ...', end='')
        while True:
            fight_finish = auto_adb.check('temp_images/fight-finish.png')
            if fight_finish:
                print(' 战斗结束 !')
                auto_adb.click_finally('temp_images/fight-finish.png')
                auto_adb.click_finally('temp_images/fight-finish-1.png')
                auto_adb.click_finally('temp_images/fighting-finish-1.5.png', max_wait_time=3)
                auto_adb.click_finally('temp_images/fight-finish-2.png')
                time.sleep(3)
                break
            print('...', end='')


# 招惹敌军
def provoke_enemy(auto_adb):
    image_dir = 'temp_images/enemy'
    image_name_list = os.listdir(image_dir)

    find_enemy = False
    for image_name in image_name_list:
        image_rel_path = image_dir + '/' + image_name
        find_enemy = auto_adb.click(image_rel_path)
        if find_enemy:
            return True
    if not find_enemy:
        # todo 尝试滑动界面
        print('找不到敌机')
        return False


# 选择关卡
def pick_round():
    auto_adb = AutoAdb()
    check = auto_adb.check('temp_images/in-round.png')
    if check:
        return

    # 确定进入
    auto_adb.click('temp_images/round/3-1.png')
    auto_adb.click('temp_images/fight-confirm.png')
    auto_adb.click('temp_images/fight-confirm.png')


# 回到主页
def go_to_main_page():
    auto_adb = AutoAdb()
    while True:
        check = auto_adb.check('temp_images/main-fight.png')
        if check:
            print('已回到主页')
            break
        res = auto_adb.click('temp_images/home-page.png')
        if not res:
            print('无法回到首页, 请手动调整 ...')


if __name__ == '__main__':
    # 保证配置优先初始化
    config.init_config()
    AutoAdb(test_device=True)
    run()
