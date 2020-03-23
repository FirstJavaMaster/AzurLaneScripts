from common import StageFight
from common.AutoAdb import AutoAdb

if __name__ == '__main__':
    auto_adb = AutoAdb(test_device=True)
    res = auto_adb.check('temp_images/stage/in-stage.png')
    if res:
        StageFight.fight_in_stage()
