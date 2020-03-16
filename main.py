import time
from datetime import datetime

import config
from common import TempUtils, Swiper
from common.AutoAdb import AutoAdb
from common.Location import Location


def run():
    auto_adb = AutoAdb()

    # 如果已经在某个关卡中了, 那就先战斗
    res = auto_adb.check('temp_images/stage/in-stage.png')
    if res:
        fight_in_stage()

    # 关卡出击
    while True:
        # 选择关卡
        pick_stage()
        # 开始战斗
        fight_in_stage()


def fight_in_stage():
    auto_adb = AutoAdb()
    while True:
        # 寻找敌人
        res = provoke_enemy()
        if not res:
            break

        print('战斗开始 >>>')
        auto_adb.wait('temp_images/fight/fight-finish.png')
        print(' 战斗结束 !')
        ending_loc = Location(auto_adb, None, 1040, 660)
        while True:
            in_stage = auto_adb.check('temp_images/stage/in-stage.png')
            in_unit = auto_adb.check('temp_images/stage/in-unit.png')
            if in_stage or in_unit:
                break

            new_ship = auto_adb.check('temp_images/fight/new-ship.png')
            if new_ship:
                input('发现新船!! 按下任何按键以继续 ...')
                continue
            ending_loc.click()

        # 可能出现紧急任务提示
        # 由于是透明遮罩, 所以无法根据其他元素是否显示而做出反应, 只能等一定的时间
        auto_adb.wait('temp_images/fight/urgent-task.png', max_wait_time=3).click()


# 招惹敌军.
# True 说明已经找到
# False 说明关卡结束
# 异常退出 说明关卡未结束, 可是无法分辨出敌人
def provoke_enemy():
    # 这里要多等待几秒, 因为经常会有个动画影响寻敌
    time.sleep(3)

    auto_adb = AutoAdb()
    check = auto_adb.check('temp_images/stage/in-unit.png')
    if check:
        print('关卡已经结束')
        return False

    # 切换到第二舰队
    if auto_adb.check('temp_images/stage/bullet-empty.png'):
        auto_adb.wait('temp_images/stage/switch-over.png').click(2)

    image_rel_path_list = TempUtils.get_temp_rel_path_list('temp_images/enemy')

    swipe_times = 0
    while True:
        print('寻找敌人 ... ')
        enemy_loc = auto_adb.get_location(*image_rel_path_list)
        if enemy_loc is None:
            swipe_times += 1
            print('未找到敌人, 尝试滑动页面 %d' % swipe_times)
            Swiper.swipe(swipe_times)
            continue

        # 如果找到的是boss, 且当前是第一队, 则放弃此敌人, 重新寻找敌人
        is_boss = enemy_loc.temp_rel_path == 'temp_images/enemy/z-boss.png'
        is_first_team = auto_adb.check('temp_images/stage/team-1.png')
        if is_boss and is_first_team:
            image_rel_path_list.remove(enemy_loc.temp_rel_path)
            continue

        enemy_loc.click()
        # 等待进击按钮出现, 期间会不断处理意外情况, 如果指定时间内出现按钮, 则执行结束, 否则再次循环
        res = auto_adb.wait('temp_images/fight/fight.png', max_wait_time=8,
                            episode=deal_accident_when_provoke_enemy).click()
        if res:
            check_port_full()
            return True
        else:
            # 如果点击后未进入确认界面, 说明那里不可到达, 此时去除image_rel_path_list中的值
            image_rel_path_list.remove(enemy_loc.temp_rel_path)


# 处理进击时的意外情况
def deal_accident_when_provoke_enemy():
    auto_adb = AutoAdb()
    # 自动战斗
    res = auto_adb.click('temp_images/fight/auto-fight-confirm-1.png')
    if res:
        print('确认自律战斗')
        auto_adb.wait('temp_images/fight/auto-fight-confirm-2.png').click()
    # 处理途中获得道具的提示
    auto_adb.click('temp_images/stage/get-tool.png')
    # 处理伏击
    auto_adb.click('temp_images/stage/escape.png')


# 选择关卡
def pick_stage():
    # 判断港口是否满员
    check_port_full()

    auto_adb = AutoAdb()
    # 判断是否已经在关卡中
    res = auto_adb.wait('temp_images/stage/in-stage.png', max_wait_time=2).is_valuable()
    if res:
        return

    # 确定进入
    target_stage_list = TempUtils.get_temp_rel_path_list('temp_images/target-stage')
    start_time = datetime.now()
    while True:
        duration = (datetime.now() - start_time).seconds
        print('\r扫描目标关卡中 ... %ds' % duration, end='')
        loc = auto_adb.get_location(*target_stage_list)
        if loc is not None:
            break

    print('%s √' % loc.temp_rel_path)
    loc.click()
    # 这里不是重复, 是确实要点两下. 一次确认关卡, 一次确认队伍
    auto_adb.wait('temp_images/stage/into-confirm.png').click()
    auto_adb.wait('temp_images/stage/into-confirm.png', episode=check_port_full).click()

    # 确保已经进入关卡
    auto_adb.wait('temp_images/stage/in-stage.png')


# 判断船坞是否满员
def check_port_full():
    auto_adb = AutoAdb()
    port_full = auto_adb.check('temp_images/port-full.png')
    if port_full:
        print('船坞已经满员了, 请整理')
        exit(1)


if __name__ == '__main__':
    # 保证配置优先初始化
    config.init_config()
    AutoAdb(test_device=True)
    run()
