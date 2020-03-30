from bin import StageFight


def run():
    # 计数
    num = 0
    # 循环战斗
    while True:
        # 选择关卡
        StageFight.pick_stage()
        # 开始战斗
        StageFight.fight_in_stage()
        # 计数
        num += 1
        print('通关次数累计：%d' % num, end='\n\n')


if __name__ == '__main__':
    print('[连发模式]启动! (持续寻找目标关卡)', end='\n\n')
    run()
