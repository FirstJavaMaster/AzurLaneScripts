from bin import StageFight
from common.AutoAdb import AutoAdb
from common.Location import Location


def to_main_page():
    adb = AutoAdb()
    temp_list = [
        'temp_images/page/main-page-button.png',  # 主页按钮
        'temp_images/page/close.png',  # 关闭按钮
        'temp_images/page/close-1.png',  # 关闭按钮
        'temp_images/page/back.png',  # 返回按钮
        'temp_images/page/back-2.png'  # 返回按钮
    ]
    while True:
        # 如果已经在主页则直接返回
        if in_main_page():
            return True
        # 尝试点击返回按钮
        loc = adb.get_location(*temp_list)
        if loc is None:  # 如果没找到合理的返回按钮，则点击左上角尝试
            Location(adb, None, 10, 10).click()
        else:
            loc.click()


def to_stage_page():
    adb = AutoAdb()
    if in_stage_page():
        return True

    to_main_page()
    adb.click('temp_images/page/main-fight.png')
    # 可能正处在战斗关卡，自动战斗
    fight = StageFight.wind_up_stage_fight()
    if fight:
        return to_stage_page()
    return True


def back():
    temp_list = [
        'temp_images/page/back.png',  # 返回按钮
        'temp_images/page/back-2.png'  # 返回按钮
    ]
    loc = AutoAdb().get_location(*temp_list)
    if loc is not None:
        print('点击页面返回按钮')
        loc.click()


def in_main_page():
    return AutoAdb().check('temp_images/page/in-main.png')


def in_stage_page():
    return AutoAdb().check('temp_images/page/in-stage.png')


def in_operation_page():
    return AutoAdb().check('temp_images/page/in-operation.png')


def in_enemy_page():
    return AutoAdb().check('temp_images/page/in-enemy.png')


def in_fight_page():
    return AutoAdb().check('temp_images/page/in-fighting.png')
