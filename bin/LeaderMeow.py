from common import PageUtils
from common.AutoAdb import AutoAdb
from common.Location import Location


# 每天领取指挥喵
def run():
    adb = AutoAdb()
    PageUtils.to_main_page()
    # 点击生活区
    Location(adb, None, 580, 680).click()
    # 点击指挥喵
    Location(adb, None, 980, 460).click()
    # 判断有无免费订购。
    have_free = adb.click("temp_images/daily-task/meow/free-meow.png")
    if have_free:
        # 第二次判断
        have_free = adb.check("temp_images/daily-task/meow/free-meow-1.png")
    if have_free:
        # 领取免费
        Location(adb, None, 900, 460).click()
        # 点击确定
        Location(adb, None, 780, 450).click()
        # 二次确定
        adb.wait("temp_images/daily-task/meow/free-meow-confirm.png").click()
        # 关闭领取对话框
        Location(adb, None, 640, 700).click()

    # 点击训练
    Location(adb, None, 1200, 680).click()
    # 点击“全部完成”
    adb.wait("temp_images/daily-task/meow/finish-all.png").click(2)
    # 将所有完成提示点击掉
    while True:
        find_finish_all = adb.check("temp_images/daily-task/meow/finish-all.png")
        if find_finish_all:
            break
        Location(adb, None, 640, 20).click()

    # 点击“开始训练”
    Location(adb, None, 970, 560).click()
    # 点击“一键选择”
    adb.wait("temp_images/daily-task/meow/pick-all.png").click()
    # 点击“开始训练”
    Location(adb, None, 970, 560).click()
    # 点击确认
    adb.wait("temp_images/daily-task/meow/birth-start-confirm.png", max_wait_time=3).click()
    # 回到主页
    PageUtils.to_main_page()


if __name__ == '__main__':
    run()
