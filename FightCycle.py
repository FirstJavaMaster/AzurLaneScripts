from bin import StageFight
from common import ConfigUtils


def run():
    # 计数
    num = 0
    # 最大通关次数
    max_stage_fight_times = int(ConfigUtils.get('max_stage_fight_times'))
    # 循环战斗
    while True:
        # 选择关卡
        StageFight.pick_stage()
        # 开始战斗
        StageFight.fight_in_stage()
        # 计数
        num += 1
        print('通关次数累计：%d' % num, end='\n\n')
        if max_stage_fight_times is not None and num >= max_stage_fight_times:
            print('已达最大通关次数 %d，结束运行' % max_stage_fight_times)
            exit()


if __name__ == '__main__':
    print('[连发模式]启动! (持续寻找目标关卡)', end='\n\n')
    run()
