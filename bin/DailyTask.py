import datetime
import time

from bin import StageFight
from common import PageUtils
from common.AutoAdb import AutoAdb
from common.Location import Location


def run():
    print('每日任务开始。。。')
    print('目前仅支持 ”商船护卫“、”海域突进“、“斩首行动” 三个类别。')
    print('“战术研修”和“破交作战”由于战力要求和操控要求比较高，因此暂不能自动化。')
    print()
    adb = AutoAdb()

    task_list = [
        {'loc': Location(adb, None, 160, 400, '商船护卫'), 'day': [1, 4, 7]},
        {'loc': Location(adb, None, 370, 400, '海域突进'), 'day': [2, 5, 7]},
        {'loc': Location(adb, None, 900, 400, '斩首行动'), 'day': [3, 6, 7]}
    ]

    week_day = datetime.datetime.now().weekday() + 1
    for task in task_list:
        task_loc = task['loc']
        if week_day not in task['day']:
            continue

        PageUtils.to_stage_page()
        adb.wait('temp_images/daily-task/daily-task/goto-daily-task.png').click(2)
        task_loc.click(2)  # 点击对应模式, 移动到页面中间
        Location(adb, None, 640, 400).click()  # 点击中间, 进入模式
        # 执行方法
        print('今天是周%d，%s开放' % (week_day, task_loc.remark))
        TaskHelper(task_loc.remark).run()
    PageUtils.to_main_page()


class TaskHelper:
    adb = AutoAdb()
    task_name = None
    flag = 0
    x_pos = 450
    y_pos = 150
    y_step = 160

    def __init__(self, task_name):
        self.task_name = task_name

    def run(self):
        # 点击出击
        Location(self.adb, None, self.x_pos, self.y_pos + self.y_step * self.flag).click()
        # 观察是否已经耗尽机会
        while True:
            # 出现出击按钮，说明已经进入关卡了
            if self.adb.check('temp_images/fight/fight.png'):
                break
            # 如果出现没有机会提示，则说明没机会了
            if self.adb.check('temp_images/daily-task/daily-task/no-chance.png',
                              'temp_images/daily-task/daily-task/no-chance-2.png',
                              threshold=0.95):
                print('机会耗尽，%s结束' % self.task_name)
                return
        # 切换到最右边的队伍
        while True:
            have_right = self.adb.click('temp_images/daily-task/daily-task/right-team.png')
            if not have_right:
                break
        # 出击
        print('出击第 %d 关' % (self.flag + 1))
        result = StageFight.fight()
        if not result:
            print('挑战失败，目标下移。。。')
            self.step_add()
        # 调用自己，继续战斗
        self.run()

    def step_add(self):
        if self.flag >= 3:
            print('失败次数过多，停止战斗')
            exit()
        if self.flag < 3:
            print('关卡游标下移')
            self.flag += 1
        print('失败次数累计：%d' % self.flag)
        time.sleep(1)


if __name__ == '__main__':
    AutoAdb(test_device=True)
    run()
