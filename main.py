import os

import config
from common.AutoAdb import AutoAdb


def run():
    # 首先到主界面
    go_to_main_page()

    auto_adb = AutoAdb()
    # 主界面出击
    auto_adb.wait('temp_images/main-fight.png').click()

    # 选择关卡
    pick_round()

    while True:
        # 寻找敌人
        res = provoke_enemy()
        if not res:
            exit(1)

        # 处理自律战斗的提示
        res = auto_adb.wait('temp_images/auto-fight-confirm-1.png', max_wait_time=3).click()
        if res:
            print('确认自律战斗')
            auto_adb.wait('temp_images/auto-fight-confirm-2.png').click()

        # 找到敌人后开始出击
        auto_adb.wait('temp_images/fight.png').click()
        check_port_full()

        print('战斗开始 ...')
        fight_finish_loc = auto_adb.wait('temp_images/fight-finish.png')
        print(' 战斗结束 !')
        fight_finish_loc.click()
        auto_adb.wait('temp_images/fight-finish-1.png').click()
        auto_adb.wait('temp_images/fight-finish-1.5.png', max_wait_time=3).click()
        auto_adb.wait('temp_images/fight-finish-2.png').click(3)


# 招惹敌军
def provoke_enemy():
    auto_adb = AutoAdb()
    image_dir = 'temp_images/enemy'
    image_name_list = os.listdir(image_dir)

    for image_name in image_name_list:
        image_rel_path = image_dir + '/' + image_name
        loc = auto_adb.get_location(image_rel_path)
        if loc is not None:
            loc.click()
            # 处理途中获得道具的提示
            auto_adb.wait('temp_images/get-tool.png', max_wait_time=3).click()
            loc.click()
            return True
    # todo 尝试滑动界面
    print('找不到敌机')
    return False


# 选择关卡
def pick_round():
    auto_adb = AutoAdb()
    res = auto_adb.wait('temp_images/in-round.png', max_wait_time=5).is_valuable()
    if res:
        return

    check_port_full()
    # 确定进入
    auto_adb.wait('temp_images/round/4-3.png').click()
    auto_adb.wait('temp_images/fight-confirm.png').click()


# 判断船坞是否满员
def check_port_full():
    auto_adb = AutoAdb()
    port_full = auto_adb.check('temp_images/port-full.png')
    if port_full:
        print('船坞已经满员了, 请整理')
        exit(1)


# 回到主页
def go_to_main_page():
    auto_adb = AutoAdb()
    while True:
        check = auto_adb.check('temp_images/main-fight.png')
        if check:
            return True

        res = auto_adb.wait('temp_images/home-page.png', max_wait_time=3).click()
        if res:
            print('回到首页')
            return True
        else:
            print('未找到首页按钮, 请手动调整 ...')


if __name__ == '__main__':
    # 保证配置优先初始化
    config.init_config()
    AutoAdb(test_device=True)
    run()
