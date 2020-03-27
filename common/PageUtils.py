from common.AutoAdb import AutoAdb


def confirm_in_main_page():
    adb = AutoAdb()
    # 如果已经在主页则直接返回
    check = adb.check("temp_images/main-page.png")
    if check:
        return True

    # 点击关闭按钮
    click = adb.click("temp_images/close.png")
    if click:
        return True
    # 点击返回按钮肯定？可以到主页
    click = adb.click("temp_images/main-page-button-2.png")
    if click:
        return True
    # 点击主页按钮肯定可以到主页
    click = adb.click("temp_images/main-page-button.png")
    if click:
        return True

    # 如果到这里了，那只能是
    return False
