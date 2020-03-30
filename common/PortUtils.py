from common import ConfigUtils
from common.AutoAdb import AutoAdb


# 判断船坞是否满员。如果未满员返回False，如果已满员且执行了退役操作，则返回True，否则终止程序
def check_port_full():
    adb = AutoAdb()
    port_full = adb.check('temp_images/port/port-full.png')
    if not port_full:
        return False

    print('船坞已经满员了... ', end='')
    auto_retire = ConfigUtils.get('auto_retire', fallback=False)
    if auto_retire:
        print('开始自动退役... ', end='')
        adb.wait('temp_images/port/port-full-retire.png').click()  # 整理
        adb.wait('temp_images/port/retire.png').click()  # 一键退役
        adb.wait('temp_images/port/retire-confirm.png').click()  # 确定舰娘
        adb.wait('temp_images/port/retire-confirm.png', max_wait_time=2).click()  # 确定（可能出现的）精英舰娘
        adb.wait('temp_images/port/retire-confirm-1.png').click()  # （获得物资）点击继续
        adb.wait('temp_images/port/retire-confirm.png').click()  # 确定装备
        adb.wait('temp_images/port/retire-confirm.png').click()  # 确定物资
        adb.wait('temp_images/port/retire-confirm-1.png').click()  # （获得物资）点击继续
        adb.wait('temp_images/port/cancel.png').click()  # （获得物资）点击继续
        print('退役完成, 程序继续执行')
        return True
    print('未启用自动退役配置, 程序退出')
    exit()
