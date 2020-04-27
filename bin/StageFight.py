from common import PortUtils, PageUtils
from common.AutoAdb import AutoAdb
from common.Location import Location
from common.TeamLeader import TeamLeader

# 选择关卡stage
from common.Timer import Timer


def fight_stage(stage_temp_list):
    if stage_temp_list is None or len(stage_temp_list) == 0:
        print('目标关卡未指定')
        exit(1)

    auto_adb = AutoAdb()
    # 判断是否已经在关卡中
    in_enemy = PageUtils.in_enemy_page()
    if in_enemy:
        fight_all_enemy()
        return

    # 确定进入
    timer = Timer()
    while True:
        print('\r扫描目标关卡中 ... %ds ' % timer.get_duration(), end='')
        loc = auto_adb.get_location(*stage_temp_list)
        if loc is not None:
            break

    print('%s √' % loc.temp_rel_path)
    loc.click()  # 点击关卡图标
    confirmed = confirm_stage_team()  # 确认队伍
    if not confirmed:  # 如果队伍确认失败，则重新做一次
        fight_stage(stage_temp_list)


# 进入关卡的确认操作。成功进入了（即使战斗失败）会返回true，否则false
def confirm_stage_team():
    adb = AutoAdb()
    timer = Timer()
    while True:
        print('\r确认关卡队伍中。。。 %ds ' % timer.get_duration(), end='')
        # 如果已经进入敌人列表界面，则跳出循环
        if PageUtils.in_enemy_page():
            print(' √')
            fight_all_enemy()  # 战斗
            return True

        button_list = [
            'temp_images/stage/immediate-start.png',  # 立刻前往
            'temp_images/stage/weigh-anchor.png',  # 出击按钮
            'temp_images/fight/fight-confirm.png'  # 特殊关卡会提示更多
        ]
        button_loc = adb.get_location(*button_list)
        if button_loc is not None:
            button_loc.click()
        port_full = PortUtils.check_port_full()
        if port_full:
            return False


# 执行关卡的战斗
def fight_all_enemy():
    team_leader = TeamLeader()
    while True:
        team_leader.provoke_enemy()
        fight_result = fight()
        # 如果在单元界面，说明关卡已经结束
        if PageUtils.in_stage_page():
            print('关卡战斗结束')
            if fight_result:
                break
            print('boss战失败 或 所有舰队均不能成型, 为避免更多损失, 脚本终止')
            exit()


# fight前确认team，监控fight，fight收尾
# 战斗胜利时返回True，失败时返回false
def fight():
    adb = AutoAdb()
    # 战斗前各种按钮的点击
    while True:
        if PageUtils.in_fight_page():
            break
        click = adb.click('temp_images/fight/fight.png')
        if click:
            continue
        retired = PortUtils.check_port_full()
        if retired:  # 如果发生了退役操作，则再次点击确认按钮
            AutoAdb().wait('temp_images/fight/fight.png').click()
            continue
        low_mood = adb.check('temp_images/fight/low-mood.png')
        if low_mood:
            print('低心情状态，脚本终止')
            exit()

    print('战斗开始 >>>')
    return fight_finish()


# 监控战斗的画面，处理战斗结束操作
# 战斗胜利时返回True，失败时返回false
def fight_finish():
    adb = AutoAdb()
    adb.wait('temp_images/fight/fight-finish.png', cycle_interval=5)

    # 战斗结束
    fight_result = None
    ending_loc = Location(adb, None, 1160, 690)
    while True:
        if fight_result is None:
            # 处理新船
            new_ship = adb.check('temp_images/fight/new-ship.png')
            if new_ship:
                print('发现新船!!')
                fight_result = True
                ending_loc.click()
                adb.click('temp_images/confirm-btn.png')
                continue
            # 处理失败
            fail_confirm = adb.click('temp_images/fight/fail-confirm.png')
            if fail_confirm:
                fight_result = False
                # 战队难以成型时点击确定
                adb.wait('temp_images/confirm-btn.png', max_wait_time=3).click()
                break
        # 持续点击右下角
        ending_loc.click()
        # 回到 stage列表页面 或 敌人列表页面 也说明战斗已经结束
        if adb.check('temp_images/page/in-stage.png',  # stage列表
                     'temp_images/page/in-enemy.png',  # enemy列表
                     'temp_images/page/in-daily.png'):  # 日常任务结束后的界面
            fight_result = True
            break
        if adb.check('temp_images/page/in-operation.png'):
            print('误入演习界面，退出。。。')
            PageUtils.back()
            continue

    print('战斗胜利~(～￣▽￣)～' if fight_result else '战斗失败 >_<')
    # 战斗结束后可能出现紧急任务提示
    # 由于是透明遮罩, 所以无法根据其他元素是否显示而做出反应, 只能等一定的时间
    adb.wait('temp_images/confirm-btn.png', max_wait_time=2).click()
    return fight_result


# 收尾关卡战斗：如果已经在关卡中，就战斗至结束
# 如果发生了战斗，则返回True，否则False
def wind_up_stage_fight():
    if PageUtils.in_fight_page():
        print('正在战斗。。。')
        fight_finish()

    if PageUtils.in_enemy_page():
        print('扫荡剩余敌军。。。')
        fight_all_enemy()
        return True
    return False
