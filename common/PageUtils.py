from common.AutoAdb import AutoAdb
from common.Location import Location


def to_main_page():
    adb = AutoAdb()
    temp_list = [
        'temp_images/close.png',  # 关闭按钮
        'temp_images/main-page-button-2.png',  # 返回按钮
        'temp_images/main-page-button.png'  # 主页按钮
    ]
    while True:
        # 如果已经在主页则直接返回
        if adb.check("temp_images/main-page.png"):
            return True
        # 尝试点击返回按钮
        loc = adb.get_location(*temp_list)
        if loc is None:  # 如果没找到合理的返回按钮，则点击左上角尝试
            Location(adb, None, 18, 18).click()
        else:
            loc.click()
