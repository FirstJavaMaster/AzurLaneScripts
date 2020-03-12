# AzurLaneScripts

碧蓝航线的自动刷图脚本.

tips_1: 电脑需要安装python运行环境.
 
tips_2: 需要 ADB + 安卓模拟器/手机 配合使用.

tips_3: 默认读者已经有一定的编程基础.

tips_4: 脚本还在完善中, 配置运行方式都可能会(向着更简便的方式)改变.

## 使用方法

这里仅讨论windows平台的使用

### 环境搭建

#### 安装python

前往 [miniconda](https://docs.conda.io/en/latest/miniconda.html) 下载 python 3.7 安装包并安装.

安装时注意配置运行环境(path).

    如何判断python安装成功?
    
    打开cmd, 执行 `python --version`, 如果正确显示python版本号则说明安装成功

#### 脚本下载和配置

下载本项目到本地, 修改 `config.py` 文件中的 `adb_path` 后的值为本地的adb.exe所在路径.

安装ADB的方法请参考 [微信跳一跳脚本的教程](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4).


### 运行

打开游戏, 进入游戏主界面. 然后运行脚本 `main.py`