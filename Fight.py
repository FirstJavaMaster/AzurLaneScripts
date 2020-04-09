from bin import StageFight
from common.AutoAdb import AutoAdb

if __name__ == '__main__':
    AutoAdb(test_device=True)
    print('[单发模式] 如果已经在某个关卡中，则自动战斗至关卡结束', end='\n\n')
    res = StageFight.wind_up_stage_fight()
    if res:
        print('关卡收尾结束')
    else:
        print('未在关卡中，结束运行')
