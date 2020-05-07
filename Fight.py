from bin import StageFight
from common import ConfigUtils, PathUtils
from common.AutoAdb import AutoAdb
from common.FightRecorder import FightRecorder


def run():
    # 计数
    fight_recorder = FightRecorder()
    # 最大通关次数
    max_stage_fight_times = int(ConfigUtils.get('max_stage_fight_times'))
    # 循环战斗
    while True:
        # 选择关卡 开始战斗
        target_stage_list = PathUtils.get_temp_rel_path_list('temp_images/target-stage')
        fight_result = StageFight.fight_stage(target_stage_list)
        # 计数
        fight_recorder.append(fight_result)
        fight_recorder.print_recorder()
        # 连续失败两次就停止战斗
        if fight_recorder.get_last_fail_count() >= 2:
            print('连续 2 次关卡战斗失败, 为了避免更多损失脚本自动退出')
            exit()
        if max_stage_fight_times is not None and fight_recorder.get_total_count() >= max_stage_fight_times:
            print('已达最大通关次数 %d，结束运行' % max_stage_fight_times)
            exit()


if __name__ == '__main__':
    AutoAdb(test_device=True)
    print('[连发模式] 持续寻找目标关卡', end='\n\n')
    run()
