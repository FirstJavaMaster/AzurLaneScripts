from common.AutoAdb import AutoAdb
from common.Slider import Slider


# 判断当前是第几个队伍
# 此操作会导致地图发生位移！！因此，此方法被调用前的位置信息会失效
def get_team_num():
    # 先滑动到地图最左边
    Slider().slide_unidirectional(4, 2)

    adb = AutoAdb()
    is_team_1 = adb.check("temp_images/stage/team-1.png")

    # 滑动回来
    Slider().slide_unidirectional(3, 1)

    # 判断
    if is_team_1:
        return 1
    return 2


# 切换队伍。
def switch():
    AutoAdb().click("temp_images/stage/team-switch.png")
