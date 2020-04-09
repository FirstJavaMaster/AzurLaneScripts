from bin import StageFight
from common import PageUtils
from common.AutoAdb import AutoAdb


def run():
    adb = AutoAdb()
    # 如果已经在关卡中，则先战斗
    StageFight.wind_up_stage_fight()

    PageUtils.to_unit_page()
    while True:
        res = deal_sos_sign(adb)
        if not res:
            print('所有求救信号已处理完毕')
            PageUtils.to_main_page()
            break


def deal_sos_sign(adb):
    adb.wait('temp_images/sos/sos-signal.png').click()

    # 将已经开启的潜艇关卡解决掉
    goto_stage_page = adb.click('temp_images/sos/goto-stage-page.png')
    if goto_stage_page:
        # 有些情况会直接进入关卡，因此不需要“点击关卡”
        print('发现已经开启的关卡，即将进入战斗。。。')
        if not StageFight.in_stage_already():
            StageFight.pick_stage(['temp_images/sos/stage-icon.png'])
        StageFight.fight_in_stage()
        return True
    # 搜索新的信号
    print('搜索新的信号。。。')
    adb.click('temp_images/sos/search-signal.png')
    searched = adb.wait('temp_images/confirm-btn.png', max_wait_time=5).click()
    if not searched:  # 如果没有搜索到，则说明已经没有信号了
        return False
    StageFight.pick_stage(['temp_images/sos/stage-icon.png'])
    StageFight.fight_in_stage()
    return True


if __name__ == '__main__':
    run()
