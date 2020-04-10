import datetime
import time

from bin import StageFight
from common import PageUtils
from common.AutoAdb import AutoAdb
from common.Location import Location


def run():
    adb = AutoAdb()

    task_list = [
        {'loc': Location(adb, None, 160, 400, '商船护卫'), 'day': [1, 4, 7], 'fuc': s_c_h_w},
        {'loc': Location(adb, None, 370, 400, '海域突进'), 'day': [2, 5, 7], 'fuc': h_y_t_j},
        {'loc': Location(adb, None, 900, 400, '斩首行动'), 'day': [3, 6, 7], 'fuc': z_s_x_d}
    ]

    week_day = datetime.datetime.now().weekday() + 1
    print('今天是周', week_day)
    for task in task_list:
        loc = task['loc']
        if week_day not in task['day']:
            continue

        PageUtils.to_unit_page()
        adb.wait('temp_images/daily-task/daily-task/goto-daily-task.png').click()
        print(loc.remark + '...已开放')
        loc.click()
        Location(adb, None, 640, 400).click()
        # 执行方法
        task['fuc']()
    PageUtils.to_main_page()


# 商船护卫
def s_c_h_w():
    print('商船护卫开始。。。')
    helper = TaskHelper()
    while True:
        helper.fight()


# 海域突进
def h_y_t_j():
    print('海域突进开始')
    adb = AutoAdb()
    helper = TaskHelper()
    while True:
        no_chance = adb.check('temp_images/daily-task/daily-task/no-chance.png')
        if no_chance:
            print('机会耗尽，关卡结束')
            break
        helper.fight()


# 斩首行动
def z_s_x_d():
    print('斩首行动开始')
    pass


class TaskHelper:
    adb = AutoAdb()
    flag = 3
    x_pos = 450
    y_pos = 150
    y_step = 160

    def fight(self):
        print('出击第 %d 关' % (self.flag + 1))
        Location(self.adb, None, self.x_pos, self.y_pos + self.y_step * self.flag).click()
        # 切换到最右边的队伍
        while True:
            have_right = self.adb.click('temp_images/daily-task/daily-task/right-team.png')
            if not have_right:
                break
        # 出击
        result = StageFight.fight()
        if not result:
            print('挑战失败，目标下移。。。')
            self.step_add()

    def step_add(self):
        if self.flag < 3:
            print('关卡游标下移')
            self.flag += 1
        print('失败次数累计：%d' % self.flag)
        time.sleep(1)


if __name__ == '__main__':
    run()
