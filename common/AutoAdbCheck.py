import subprocess

from common import ConfigUtils


def test_device(auto_adb):
    print('ADB PATH >>>> ' + auto_adb.adb_path, end='\n\n')
    try:
        subprocess.Popen([auto_adb.adb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        print('ADB 路径错误')
        exit(1)

    check_link(auto_adb)
    check_size(auto_adb)
    check_other(auto_adb)
    print('\n')


def check_link(auto_adb):
    print('检查设备 ...')
    device_number = check_link_number(auto_adb)
    if device_number < 1:
        adb_host_port = ConfigUtils.get('adb_host_port')
        if adb_host_port is not None:
            auto_adb.run('connect %s' % adb_host_port)
            device_number = check_link_number(auto_adb)

    if device_number < 1:
        print('未连接到设备, 请参考 https://github.com/FirstJavaMaster/AzurLaneScripts/blob/master/README.md')
        exit(1)
    if device_number > 2:
        print('设备数量过多, 请参考 https://github.com/FirstJavaMaster/AzurLaneScripts/blob/master/README.md')
        exit(1)
    print('设备已连接', end='\n\n')


def check_link_number(auto_adb):
    command_list = [auto_adb.adb_path, 'devices']
    process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.communicate()
    lines = output[0].decode('utf8').splitlines()
    return len(lines) - 1  # -1 是为了去除"标题行"


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
