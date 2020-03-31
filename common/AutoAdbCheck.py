import subprocess

from common import ConfigUtils


def test_device(auto_adb):
    print('ADB PATH >>>> ' + auto_adb.adb_path)
    try:
        subprocess.Popen([auto_adb.adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        print('ADB 路径错误')
        exit(1)

    check_link(auto_adb)
    check_size(auto_adb)
    check_other(auto_adb)
    print()


def check_link(auto_adb):
    adb_host_port = ConfigUtils.get('adb_host_port')
    print('检测设备连接状态 >>> %s ...' % adb_host_port)

    auto_adb.run('connect %s' % adb_host_port)
    device_list = get_devices(auto_adb)
    if len(device_list) == 0:
        print('未检测到设备，请检查ADB地址配置，或参考 https://github.com/FirstJavaMaster/AzurLaneScripts/blob/master/README.md')
        exit(1)

    exist = False
    print()
    print('设备列表：')
    for device in device_list:
        print(device)
        if adb_host_port == device:
            exist = True
    if not exist:
        print('设备列表中没找到目标连接（%s），请检查配置是否正确')
        exit(1)

    print('设备已连接', end='\n\n')


# 获取设备列表
def get_devices(auto_adb):
    new_lines = []
    lines = auto_adb.run('devices').splitlines()

    del (lines[0])  # 删除第一个标题行
    for line in lines:
        new_lines.append(line.split()[0])
    return new_lines


def check_size(auto_adb):
    output = auto_adb.run('shell wm size')
    print('屏幕分辨率: ' + output)
    if 'Physical size: 1280x720' not in output:
        print('请将分辨率设置为 1280x720 (横向 平板模式)')
        exit(1)


def check_other(auto_adb):
    output = auto_adb.run('shell wm density')
    print("像素密度: " + output)
    output = auto_adb.run('shell getprop ro.product.device')
    print("系统类型: " + output)
    output = auto_adb.run('shell getprop ro.build.version.release')
    print('系统版本: ' + output)
