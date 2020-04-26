from common import PageUtils
from common.AutoAdb import AutoAdb


# 委托任务
# todo 尚未完成
def run():
    PageUtils.to_main_page()

    adb = AutoAdb()
    adb.click('temp_images/daily-task/left-notice.png')
    complete = adb.get_location('temp_images/daily-task/delegation/complete.png').click()
    if not complete:
        print('没有委托任务')
        return

    while True:
        success_temp = [
            'temp_images/daily-task/delegation/success.png',  # 委托成功
            'temp_images/daily-task/delegation/success-1.png'  # 点击继续
        ]
        success = adb.get_location(*success_temp).click()
        if not success:
            break


if __name__ == '__main__':
    print('！！！未完成脚本！！！')
    run()
