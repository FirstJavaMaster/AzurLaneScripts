import os

import config
from common.AutoAdb import AutoAdb


def run():
    # 首先到主界面
    go_to_main_page()

    auto_adb = AutoAdb()
    # 主界面出击
    auto_adb.wait('temp_images/main-fight.png').click()
    # 关卡出击
    while True:
        go_unit()


def go_unit():
    auto_adb = AutoAdb()
    # 选择关卡
    pick_round()

    while True:
        # 寻找敌人
        res = provoke_enemy()
        if not res:
            break

        # 找到敌人后开始出击
        auto_adb.wait('temp_images/fight/fight.png').click()
        check_port_full()

        print('战斗开始 >>>')
        fight_finish_loc = auto_adb.wait('temp_images/fight/fight-finish.png')
        print(' 战斗结束 !')
        fight_finish_loc.click()
        auto_adb.wait('temp_images/fight/fight-finish-1.png').click()
        auto_adb.wait('temp_images/fight/fight-finish-2.png',
                      episode=lambda: auto_adb.click('temp_images/fight/new-ship.png')).click(3)
        # 可能出现紧急任务
        auto_adb.wait('temp_images/fight/urgent-task.png', max_wait_time=2).click()


# 招惹敌军.
# True 说明已经找到
# False 说明关卡结束, 未找到
# 异常退出 说明关卡未结束, 可是无法分辨出敌人
def provoke_enemy():
    auto_adb = AutoAdb()
    image_dir = 'temp_images/enemy'
    image_name_list = os.listdir(image_dir)

    while True:
        image_rel_path_list = map(lambda image_name: image_dir + '/' + image_name, image_name_list)
        enemy_loc = auto_adb.get_location2(*image_rel_path_list)
        if enemy_loc is None:
            check = auto_adb.check('temp_images/round/in-unit.png')
            if check:
                print('关卡已经结束')
                return False
            else:
                print('关卡未结束但找不到敌人')
                exit(1)

        enemy_loc.click()
        # 等待进击按钮出现, 期间会不断处理意外情况, 如果指定时间内出现按钮, 则执行结束, 否则再次循环
        is_valuable = auto_adb.wait('temp_images/fight/fight.png', max_wait_time=5,
                                    episode=deal_accident_when_provoke_enemy).is_valuable()
        if is_valuable:
            return True


# 处理进击时的意外情况
def deal_accident_when_provoke_enemy():
    auto_adb = AutoAdb()
    # 自动战斗
    res = auto_adb.click('temp_images/fight/auto-fight-confirm-1.png')
    if res:
        print('确认自律战斗')
        auto_adb.wait('temp_images/fight/auto-fight-confirm-2.png').click()
    # 处理途中获得道具的提示
    auto_adb.click('temp_images/round/get-tool.png')
    # 处理伏击
    auto_adb.click('temp_images/round/escape.png')


# 选择关卡
def pick_round():
    # 判断港口是否满员
    check_port_full()

    auto_adb = AutoAdb()
    # 判断是否已经在关卡中
    res = auto_adb.wait('temp_images/round/in-round.png', max_wait_time=2).is_valuable()
    if res:
        return

    # 确定进入
    auto_adb.wait('temp_images/round/4-2.png').click()
    # 这里不是重复, 是确实要点两下. 一次确认关卡, 一次确认队伍
    auto_adb.wait('temp_images/round/into-confirm.png').click()
    auto_adb.wait('temp_images/round/into-confirm.png').click()

    # 确保已经进入关卡
    auto_adb.wait('temp_images/round/in-round.png')


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

        res = auto_adb.click('temp_images/home-page.png')
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
