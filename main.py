import config
from common.AutoAdb import AutoAdb


def run():
    auto_adb = AutoAdb()
    auto_adb.screen_cap()

    res = auto_adb.click('main-fight.png')
    print(res)


if __name__ == '__main__':
    # 保证配置优先初始化
    config.__init_file__()
    run()
