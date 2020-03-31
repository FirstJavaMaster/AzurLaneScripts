from datetime import datetime

from common import PortUtils, PathUtils
from common.AutoAdb import AutoAdb
from common.Location import Location
from common.TeamLeader import TeamLeader


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


# 选择关卡
def pick_stage():
    auto_adb = AutoAdb()
    # 判断是否已经在关卡中
    res = auto_adb.wait('temp_images/stage/in-stage.png', max_wait_time=2).is_valuable()
    if res:
        return

    # 确定进入
    target_stage_list = PathUtils.get_temp_rel_path_list('temp_images/target-stage')
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
    auto_adb.wait('temp_images/stage/into-confirm.png', episode=PortUtils.check_port_full).click()
    # 特殊关卡会提示更多
    auto_adb.wait('temp_images/fight/fight-confirm.png', max_wait_time=3).click()

    # 确保已经进入关卡
    auto_adb.wait('temp_images/stage/in-stage.png')
