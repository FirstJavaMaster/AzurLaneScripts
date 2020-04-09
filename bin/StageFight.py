from datetime import datetime

from common import PortUtils
from common.AutoAdb import AutoAdb
from common.Location import Location
from common.TeamLeader import TeamLeader


# 选择关卡
def pick_stage(stage_temp_list):
    if stage_temp_list is None or len(stage_temp_list) == 0:
        print('目标关卡未指定')
        exit(1)

    auto_adb = AutoAdb()
    # 判断是否已经在关卡中
    in_stage = in_stage_already()
    if in_stage:
        return

    # todo 这部分要转移到新的脚本中
    # 如果发现现在在困难关卡，且次数为0，则终止
    if auto_adb.click('temp_images/no-chance-for-hard.png'):
        print('困难关卡机会已用尽，程序终止')
        exit()

    # 确定进入
    start_time = datetime.now()
    while True:
        duration = (datetime.now() - start_time).seconds
        print('\r扫描目标关卡中 ... %ds ' % duration, end='')
        loc = auto_adb.get_location(*stage_temp_list)
        if loc is not None:
            break

    print('%s √' % loc.temp_rel_path)
    loc.click()  # 点击关卡图标

    while True:
        in_stage = auto_adb.check('temp_images/stage/in-stage.png')
        if in_stage:
            break

        button_list = [
            'temp_images/stage/immediate-start.png',  # 立刻前往
            'temp_images/fight/fight-confirm.png'  # 特殊关卡会提示更多
        ]
        button_loc = auto_adb.get_location(*button_list)
        if button_loc is not None:
            button_loc.click()
        PortUtils.check_port_full()


# 判断是否已经在关卡中
def in_stage_already(max_wait_time=2):
    return AutoAdb().wait('temp_images/stage/in-stage.png', max_wait_time=max_wait_time).is_valuable()


# 执行关卡的战斗
def fight_in_stage():
    auto_adb = AutoAdb()
    team_leader = TeamLeader()
    while True:
        # 寻找敌人
        res = team_leader.provoke_enemy()
        if not res:
            break

        print('战斗开始 >>>')
        auto_adb.wait('temp_images/fight/fight-finish.png', cycle_interval=5)
        print(' 战斗结束 !')
        ending_loc = Location(auto_adb, None, 1160, 690)
        while True:
            in_stage = auto_adb.check('temp_images/stage/in-stage.png')
            in_unit = auto_adb.check('temp_images/stage/in-unit.png')
            if in_stage or in_unit:
                break

            new_ship = auto_adb.check('temp_images/fight/new-ship.png')
            if new_ship:
                print('发现新船!!')
                ending_loc.click()
                auto_adb.click('temp_images/fight/new-ship-confirm.png')
                continue

            fail_confirm = auto_adb.click('temp_images/fight/fail-confirm.png')
            if fail_confirm:
                print('战斗失败！！')
                # 战队难以成型时点击确定
                auto_adb.wait('temp_images/fight/fail-confirm-2.png', max_wait_time=3).click()
                continue

            ending_loc.click()

        # 可能出现紧急任务提示
        # 由于是透明遮罩, 所以无法根据其他元素是否显示而做出反应, 只能等一定的时间
        auto_adb.wait('temp_images/fight/urgent-task.png', max_wait_time=3).click()


# 收尾关卡战斗：如果已经在关卡中，就战斗至结束
# 如果发生了战斗，则返回True，否则False
def wind_up_stage_fight():
    if in_stage_already():
        print('将正在进行的关卡收尾。。。')
        fight_in_stage()
        return True
    return False
