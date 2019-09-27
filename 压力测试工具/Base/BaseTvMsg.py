import os
import time
import re
import subprocess


def stop_monkey(device):
    monkey_name = "com.android.commands.monkey"
    print("--------------------")
    pid = subprocess.Popen("adb -s " + device + " shell ps | findstr " + monkey_name, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    if pid == " ":
        print("No monkey running in %s" % device)
    else:
        for item in pid:
            if item.split()[8].decode() == monkey_name:
                monkey_pid = item.split()[1].decode()
                cmd_monkey = "adb -s " + device + " shell kill %s" % monkey_pid
                os.popen(cmd_monkey)
                print("Monkey in %s was killed" % device)
                time.sleep(2)
    subprocess.Popen("taskkill /f /t /im python学习.exe", shell=True)


def reboot(device):
    cmd_reboot = "adb -s " + device + " reboot"
    os.popen(cmd_reboot)


def getModel(devices):
    result = {}
    cmd = "adb -s " + devices + " shell cat /system/build.prop"
    print(cmd)
    # output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    output = subprocess.check_output(cmd).decode()
    result["release"] = re.findall("version.release=(\d\.\d)*", output, re.S)[0]  # Android 系统，如anroid 4.0
    result["tv_name"] = re.findall("ro.product.model=(\S+)*", output, re.S)[0]  # 机器品牌
    result["tv_model"] = re.findall("ro.product.brand=(\S+)*", output, re.S)[0]  # 芯片品牌
    return result


def get_men_total(devices):
    cmd = "adb -s " + devices + " shell cat /proc/meminfo"
    print(cmd)
    output = subprocess.check_output(cmd).split()
    return int(output[1].decode())


# 获取cpu内核数量
def get_cpu_kel(devices):
    cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
    print(cmd)
    output = subprocess.check_output(cmd).split()
    sitem = ".".join([x.decode() for x in output])  # 转换为string
    return str(len(re.findall("processor", sitem))) + "核"


# 获取设备分辨率
def get_tv_pix(devices):
    cmd = "adb -s " + devices + " shell wm size"
    print(cmd)
    return subprocess.check_output(cmd).split()[2].decode()


# 获取设备基本信息
def get_tv_Kernel(devices):
    pix = get_tv_pix(devices)
    men_total = get_men_total(devices)
    phone_msg = getModel(devices)
    cpu_sum = get_cpu_kel(devices)
    return phone_msg, men_total, cpu_sum, pix


if __name__ == '__main__':
    stop_monkey("192.168.36.108")
    print(getModel("192.168.36.108"))
    print(get_men_total("192.168.36.108"))
    print(get_tv_pix("192.168.36.108"))
    print(get_tv_Kernel("192.168.36.108"))
