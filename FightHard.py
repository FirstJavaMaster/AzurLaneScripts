from bin import StageFight
from common import PathUtils
from common.AutoAdb import AutoAdb


# 困难关卡
def run():
    StageFight.wind_up_stage_fight()

    adb = AutoAdb(test_device=True)
    temp_list = PathUtils.get_temp_rel_path_list('temp_images/target-stage-hard')
    while True:
        # 如果发现次数为0，则终止
        if adb.click('temp_images/no-chance-for-hard.png'):
            print('困难关卡机会已用尽，程序终止')
            break
        StageFight.fight_stage(temp_list)
    print('困难关卡已经结束')


if __name__ == '__main__':
    print('[困难模式] 持续寻找困难关卡', end='\n\n')
    run()
