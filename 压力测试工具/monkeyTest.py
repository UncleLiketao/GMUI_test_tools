# -*- coding: utf-8 -*-
import subprocess
import shutil
import datetime
import time
import os
from Base.BasePickle import writeInfo, writeSum, readInfo
from Base.BaseWriteReport import report
from multiprocessing import Pool
from Base.BaseFile import OperateFile
from Base import AdbCommon
from Base import BaseMonkeyConfig
from Base import BaseTvMsg
from Base import BaseMonitor

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

ba = AdbCommon.AndroidDebugBridge()

info = []


# 获取tv基础信息
def get_tv(devices):
    bg = BaseTvMsg.get_tv_Kernel(devices)
    app = {"tv_name": bg[0]["tv_name"] + "_" + bg[0]["tv_model"] + "_" + bg[0]["release"],
           "pix": bg[3],
           "rom": bg[1],
           "kel": bg[2]}
    return app


# 创建持久性文件
def mkdirInit(device, app, data=None):
    cpu = PATH("./info/" + device + "_cpu.pickle")
    men = PATH("./info/" + device + "_men.pickle")
    battery = PATH("./info/" + device + "_battery.pickle")
    fps = PATH("./info/" + device + "_fps.pickle")
    app[device] = {"cpu": cpu, "men": men, "battery": battery, "fps": fps, "header": get_tv(device)}
    OperateFile(cpu).mkdir_file()
    OperateFile(men).mkdir_file()
    OperateFile(battery).mkdir_file()
    OperateFile(fps).mkdir_file()
    OperateFile(PATH("./info/sumInfo.pickle")).mkdir_file()  # 用于记录是否已经测试完毕，里面存的是一个整数
    OperateFile(PATH("./info/info.pickle")).mkdir_file()  # 用于记录统计结果的信息，是[{}]的形式
    writeSum(0, data, PATH("./info/sumInfo.pickle"))  # 初始化记录当前真实连接的设备数


def start(devicess):
    devices = devicess["devices"]
    num = devicess["num"]
    app = {}
    mkdirInit(devices, app, num)
    mc = BaseMonkeyConfig.monkeyConfig(PATH("monkey.ini"))
    now = datetime.datetime.now().strftime('%b-%d-%Y-%H-%M-%S')
    mc["log"] = PATH("./log") + "\\" + now
    mc["monkey_log"] = mc["log"] + "monkey.log"
    mc["cmd"] = mc['cmd'] + mc["monkey_log"]
    start_monkey("adb -s " + devices + " shell " + mc["cmd"], mc["log"])
    time.sleep(1)
    starttime = datetime.datetime.now()
    pid = BaseMonitor.get_pid(mc["package_name"], devices)
    cpu_kel = BaseMonitor.get_cpu_kel(devices)
    beforeBattery = BaseMonitor.get_battery(devices)
    while True:
        with open(mc["monkey_log"], encoding='utf-8') as monkeylog:
            time.sleep(1)  # 每1秒采集检查一次
            BaseMonitor.cpu_rate(pid, cpu_kel, devices)
            BaseMonitor.get_men(mc["package_name"], devices)
            BaseMonitor.get_fps(mc["package_name"], devices)
            BaseMonitor.get_battery(devices)
            if monkeylog.read().count('Monkey finished') > 0:
                endtime = datetime.datetime.now()
                print(str(devices) + "测试完成")
                writeSum(1, path=PATH("./info/sumInfo.pickle"))
                app[devices]["header"]["beforeBattery"] = beforeBattery
                app[devices]["header"]["afterBattery"] = BaseMonitor.get_battery(devices)
                app[devices]["header"]["net"] = mc["net"]
                app[devices]["header"]["monkey_log"] = mc["monkey_log"]
                app[devices]["header"]["time"] = str((endtime - starttime).seconds) + "秒"
                writeInfo(app, PATH("./info/info.pickle"))
                break
    if readInfo(PATH("./info/sumInfo.pickle")) <= 0:
        print(readInfo(PATH("./info/info.pickle")))
        report(readInfo(PATH("./info/info.pickle")))
        subprocess.Popen("taskkill /f /t /im adb.exe", shell=True)


def runnerPool():
    shutil.rmtree((PATH("./info/")))  # 删除持久化目录
    os.makedirs(PATH("./info/"))  # 创建持久化目录
    devices_Pool = []
    devices = ba.attached_devices()
    if devices:
        for item in range(0, len(devices)):
            _app = {"devices": devices[item],
                    "num": len(devices)}
            devices_Pool.append(_app)
        pool = Pool(len(devices))
        pool.map(start, devices_Pool)
        pool.close()
        pool.join()
    else:
        print("设备不存在")


# 开始脚本测试
def start_monkey(cmd, log):
    # Monkey测试结果日志:monkey_log
    os.popen(cmd)
    print(cmd)

    # Monkey时设备日志logcatv
    logcatname = log + r"logcat.log"
    cmd2 = "adb shell cat /sdcard/syslog/logcat.log>%s" % logcatname
    os.popen(cmd2)

    # 导出traces文件
    tracesname = log + r"traces.log"
    cmd3 = "adb shell cat /data/anr/traces.txt>%s" % tracesname
    os.popen(cmd3)

    # 导出AppError文件
    appErrorname = log + r"appError.log"
    cmd4 = "adb shell cat /data/appError.txt>%s" % appErrorname
    os.popen(cmd4)


def killport():
    os.system(PATH('./kill5037.bat'))
    os.popen("adb kill-server adb")
    os.popen("adb start-server")


if __name__ == '__main__':
    runnerPool()
