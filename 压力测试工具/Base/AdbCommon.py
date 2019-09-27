import os


class AndroidDebugBridge(object):
    def call_adb(self, command):
        command_result = ''
        command_text = 'adb %s' % command
        print(command_text)
        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line:
                break
            command_result += line
        results.close()
        return command_result

    # 检查设备连接信息
    def attached_devices(self):
        result = self.call_adb("devices")
        devices = result.partition('\n')[2].replace('\n', '').split(':5555\tdevice')
        return [device for device in devices if len(device) > 2]

    # 获取设备连接状态
    def get_state(self):
        result = self.call_adb("get-state")
        result = result.strip(' \t\n\r')
        return result or None

    # 重启
    def reboot(self, option):
        command = "reboot"
        if len(option) > 7 and option in ("bootloader", "recovery",):
            command = "%s %s" % (command, option.strip())
        self.call_adb(command)

    # 将电脑文件拷贝到设备里面
    def push(self, local, remote):
        result = self.call_adb("push %s %s" % (local, remote))
        return result

    # 推送数据到本地
    def pull(self, remote, local):
        result = self.call_adb("pull %s %s" % (remote, local))
        return result

    # 同步更新
    def sync(self, directory, **kwargs):
        command = "sync %s" % directory
        if 'list' in kwargs:
            command += " -l"
            result = self.call_adb(command)
            return result

    # 打开指定app
    def open_app(self, packagename, activity, devices):
        result = self.call_adb("-s " + devices + " shell am start -n %s/%s" % (packagename, activity))
        check = result.partition('\n')[2].replace('\n', '').split('\t ')
        if check[0].find("Error") >= 1:
            return False
        else:
            return True

    # 根据包名获取到进程id
    def get_app_pid(self, pkg_name):
        string = self.call_adb("shell ps | findstr " + pkg_name)
        if string == '':
            return "the process doesn't exist."
        result = string.split(" ")
        return result[4]


if __name__ == '__main__':
    adb = AndroidDebugBridge()
    print(adb.attached_devices())
    print(adb.get_state())
    print(adb.get_app_pid("com.gitvjimi.video"))
