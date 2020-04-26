# AzurLaneScripts

碧蓝航线的自动刷图脚本.

需要注意:
+ 电脑需要安装python运行环境.
+ 需要配合 安卓模拟器(推荐)/手机 使用.
+ 这里仅讨论windows平台的使用.
+ 默认读者已经有一定的动手能力.

功能特点:
+ [ √ ] 单发模式`FightToEnd.py`: 自动战斗至关卡结束(前提是已经处于某关卡中) 
+ [ √ ] 连发模式`Fight.py`: 根据`temp_images/target-stage`目录下指定的关卡持续战斗 
+ [ √ ] 连发困难模式`FightHard.py`: 根据`temp_images/target-stage-hard`目录下指定的困难关卡持续战斗 
+ [ √ ] 求救信号`bin/SosSignal.py`: 进行求救信号战斗, 将所有信号的战斗执行至0.
+ [ √ ] 每日任务`bin/DailyTask.py`: 进行每日战斗. 但只支持 ”商船护卫“、”海域突进“、“斩首行动” 三个类别。
+ [ √ ] 领取指挥喵`bin/LeaderMeow.py`: 每天领取训练指挥喵.
+ [ × ] 自动处理委托任务
+ [ × ] 自动处理后宅
+ [ × ] 日常任务的联动处理. 即长时间挂机监控委托任务,后宅任务等
+ [ × ] 特殊关卡移动距离限制的处理. 有移动距离限制的关卡目前暂时需要手动点击移动或点击敌人

**脚本还在完善中, 配置和运行方式都可能会(向着更简便更合理的方向)改变！！！
因此使用者每次更新代码请关注该文档的更新，运行时遇到错误先查阅文档说明，也可在issues中请求帮助。**

## 使用方法

原理是通过ADB对手机屏幕截图, 对比模板图片判断当前游戏情况, 然后通过ADB模拟点击/拖拽等操作.

### 环境搭建

#### 安装python

前往 [miniconda](https://docs.conda.io/en/latest/miniconda.html) 下载 python 3.7 安装包并安装.

安装时注意配置运行环境(path).

    如何判断python安装成功?
    
    打开cmd, 执行 `python --version`, 如果正确显示python版本号则说明安装成功

#### 安装python依赖

需要用户手动安装cv2, 用来处理图像相关的工作.

    pip install opencv-python

#### 关于ADB和设备

本项目已经自带了adb.exe程序. 用户不必再手动下载.

许多安卓模拟器也会自带adb程序, 不过其自带的版本往往比较低, 一些功能残缺. 因此程序默认使用自带的adb程序。

+ 需要用户查找当前模拟器的ADB连接端口。然后修改配置文件 `config.ini` 中 `adb_host_port` 配置
+ 支持多设备在线时指定某设备连接地址进行操作。但务必配置 `adb_host_port`

##### 模拟器使用分享

不同的模拟器在ADB的实现细节上不同，游戏的体验上也不同。下表是近期（2020-03）的一些体验。欢迎体验的小伙伴贡献经验。

| 模拟器 | ADB端口 | 游戏体验 | 备注（CPU等资源占用情况）    |
| ------ | ------- | -------- | ---------------------------- |
| 雷电   | 5555    | 3.5      | 占用未注意，掉帧相对严重     |
| 逍遥   | 21503   | 4.5      | 占用相对较低，偶尔会卡死     |
| MUMU   | 7555    | 4        | 占用和逍遥接近，声称不会卡死 |
| 夜神   | 62001   |          |
| 蓝叠   | 5555    |          |
| 天天   | 5037    |          |

> 注：游戏体验是指运行是否流畅，掉帧是否严重等情况。1~5分，分数越高体验相对越好。打分全凭个人感受。

> 注：模拟器卡顿掉帧并不一定是模拟器的问题，这游戏优化本来就不太好。在我安卓手机上（小米Note3）运行也跟雷电模拟器一样，60帧开起来跟没开一样。


### 配置文件

第一次下载本项目时，项目根目录有一个 `config_temp.ini` 配置文件。

这个文件介绍了该项目可进行的配置项，但项目的运行**不会**使用此配置文件！

用户需要将该配置文件拷贝一份并重命名为 `config.ini`，然后自行修改配置。**只有 `config.ini` 文件的配置才会生效。**

请仔细阅读配置项说明。

### 运行

打开游戏，进入关卡界面。比如：

![](./wiki/unit.png)

如果你想自动刷**4-4**关卡，则将**4-4**的关卡截一个图放到 `temp_images/target-stage` 下，如：

![](./wiki/4-4.png)

**注意：**

+ temp_images/target-stage 存放普通关卡的模板文件
+ temp_images/target-stage-hard 存放困难关卡的模板文件

之所以分到两个文件夹是因为其模板图片在两种模式下往往是一样的，脚本会混淆两种模式。

然后运行 `Fight.py` 或 `FightToEnd.py` 等，各脚本的区别见上文描述。

> 战斗脚本都会自动判断是否已经在关卡中（寻敌界面），如果在就会立刻开始寻敌。因此用户可以手动点进一些特殊关卡，然后运行 `FightToEnd.py` 用来通关。


### 战斗遇敌逻辑

脚本支持”道中队“和”boss队“的设定，也支持单队的设定。

第一支队伍发现Boss后，会尝试切换到第二支队伍，然后重新寻敌。待再次遇到Boss时便会发起进攻。

注：Boss优先级比其他船只的优先级高
