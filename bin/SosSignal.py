from bin import StageFight
from common import PageUtils
from common.AutoAdb import AutoAdb


def run():
    print('处理求救信号关卡。。。')
    # 如果已经在关卡中，则先战斗
    StageFight.wind_up_stage_fight()

    PageUtils.to_stage_page()
    while True:
        res = deal_sos_sign()
        if not res:
            print('所有求救信号已处理完毕')
            PageUtils.to_main_page()
            break


def deal_sos_sign():
    adb = AutoAdb()
    adb.wait('temp_images/sos/sos-signal.png').click()

    # 将已经开启的潜艇关卡解决掉
    goto_stage_page = adb.click('temp_images/sos/goto-stage-page.png')
    if goto_stage_page:
        # 有些情况会直接进入关卡，因此不需要“点击关卡”
        print('发现已经开启的关卡，即将进入战斗。。。')
        if PageUtils.in_enemy_page():
            StageFight.fight_all_enemy()
        else:
            StageFight.fight_stage(['temp_images/sos/stage-icon.png'])
        return True
    # 搜索新的信号
    print('搜索新的信号。。。')
    adb.click('temp_images/sos/search-signal.png')
    while True:
        if adb.check('temp_images/sos/no-chance.png'):
            print('已经没有新的信号，SOS关卡执行完毕，脚本退出')
            PageUtils.to_stage_page()
            exit()

        # 如果有确认按钮，则点击确认，前往关卡
        adb.click('temp_images/confirm-btn.png')
        # 如果已经发现了关卡按钮，则点击
        click_stage = adb.click('temp_images/sos/stage-icon.png')
        if click_stage:
            print('进入SOS关卡战斗。。。')
            confirmed = StageFight.confirm_stage_team()
            if not confirmed:
                continue
            return True


if __name__ == '__main__':
    run()
