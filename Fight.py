from bin import StageFight
from common.AutoAdb import AutoAdb


def run():
    adb = AutoAdb(test_device=True)
    in_stage = adb.check('temp_images/stage/in-stage.png')
    if in_stage:  # 如果已经在关卡中，则继续战斗
        StageFight.fight_in_stage()
        return True
    return False


if __name__ == '__main__':
    print('[单发模式] 启动：如果已经在某个关卡中，则自动战斗至关卡结束', end='\n\n')
    res = run()
    if res:
        print('关卡收尾结束')
    else:
        print('未在关卡中，结束运行')
