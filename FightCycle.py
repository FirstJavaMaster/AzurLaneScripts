from common import StageFight
from common.AutoAdb import AutoAdb


def run(cycle=True):
    auto_adb = AutoAdb(test_device=True)
    res = auto_adb.check('temp_images/stage/in-stage.png')
    if res:  # 如果已经在关卡中，则继续战斗
        StageFight.fight_in_stage()

    # 循环战斗
    while True:
        # 选择关卡
        StageFight.pick_stage()
        # 开始战斗
        StageFight.fight_in_stage()
        # 判断是否循环
        if not cycle:
            break


if __name__ == '__main__':
    run()
