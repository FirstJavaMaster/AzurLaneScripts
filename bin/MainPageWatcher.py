from common import PageUtils
from common.AutoAdb import AutoAdb
from common.Location import Location


def run():
    print('日常巡检开始。。。')

    adb = AutoAdb()
    notice_loc = adb.get_location('temp_images/daily-task/notice.png')
    if not notice_loc:
        print('没有待处理的任务，巡检结束')
        return

    # 菜单位置
    menu_pos = [
        Location(adb, None, 628, 674, 'life-area'),  # 生活区
        Location(adb, None, 946, 674, 'missions'),  # 任务
    ]
    nearest_loc = notice_loc.get_nearest(menu_pos)
    nearest_loc.click()
    nearest_remark = nearest_loc.remark
    if nearest_remark == 'life-area':
        check_life_area(adb)
    elif nearest_remark == 'missions':
        deal_missions(adb)
    else:
        print('不能分辨出处理任务')


# todo 检查生活区
def check_life_area(adb):
    pass


# 领取任务奖励
def deal_missions(adb):
    print('领取任务奖励。。。')
    while True:
        have_receive_all = adb.wait('temp_images/daily-task/missions/receive-all.png').click()
        if have_receive_all:
            adb.wait('temp_images/click-to-continue.png').click()
        else:
            break
    print('领取完毕')
    PageUtils.to_main_page()


if __name__ == '__main__':
    print('！！！未完成脚本！！！')
    run()
