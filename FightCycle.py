from common import StageFight
from common.AutoAdb import AutoAdb


def run(cycle=True):
    num = 0

    auto_adb = AutoAdb(test_device=True)
    res = auto_adb.check('temp_images/stage/in-stage.png')
    if res:  # 如果已经在关卡中，则继续战斗
        num += 1
        StageFight.fight_in_stage()

    # 循环战斗
    while True:
        if not cycle and num >= 1:
            break
        # 选择关卡
        StageFight.pick_stage()
        # 开始战斗
        StageFight.fight_in_stage()


if __name__ == '__main__':
    run()
