from common import PageUtils
from common.AutoAdb import AutoAdb
from common.Location import Location


# 每天领取指挥喵
def run():
    adb = AutoAdb()
    blank_loc = Location(adb, None, 600, 30)

    PageUtils.to_main_page()
    # 点击生活区
    Location(adb, None, 580, 680).click()
    # 点击指挥喵
    Location(adb, None, 980, 460).click()
    # 判断有无免费订购。
    have_free = adb.click("temp_images/daily-task/meow/free-meow.png", threshold=0.95)
    if have_free:
        # 第二次判断
        have_free = adb.check("temp_images/daily-task/meow/free-meow-1.png", threshold=0.95)
    if have_free:
        print('领取每日免费喵箱...')
        # 结算
        adb.wait('temp_images/daily-task/meow/buy.png').click()
        # 点击确定
        adb.wait('temp_images/daily-task/meow/confirm.png').click()
        # 二次确定
        adb.wait("temp_images/click-to-continue.png").click()
        # 关闭领取对话框
        blank_loc.click()

    # 点击训练
    Location(adb, None, 1200, 680).click()
    # 等待对话框打开
    adb.wait('temp_images/daily-task/meow/in-lesson-page.png')
    while adb.click('temp_images/daily-task/meow/lesson-finish.png', wait_time=2):
        print('领取训练完成的喵...')
        while True:
            if adb.click('temp_images/daily-task/meow/new-meow-btn.png'):
                continue
            if adb.click('temp_images/daily-task/meow/confirm.png'):
                continue
            if adb.check('temp_images/daily-task/meow/in-lesson-page.png'):
                break

    print('训练新的喵...')
    # 点击“开始训练”
    adb.wait('temp_images/daily-task/meow/start-lesson.png').click()
    # 点击“一键选择”
    adb.wait("temp_images/daily-task/meow/pick-all.png").click()
    # 点击“开始训练”
    adb.wait('temp_images/daily-task/meow/start-lesson.png').click()
    # 点击确认
    adb.wait("temp_images/daily-task/meow/confirm.png", max_wait_time=3).click()
    # 回到主页
    PageUtils.to_main_page()
    print('指挥喵处理完毕')


if __name__ == '__main__':
    print('！！！未完成脚本！！！')
    run()
