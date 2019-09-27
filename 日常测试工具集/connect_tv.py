"""
TV端 连接类
"""
import os
import re


class ConnectTv:
    def __init__(self):
        self.ip = self._input

    # 输入连接设备的IP地址
    @property
    def _input(self):
        ip = input('请输入连接设备的IP地址：')
        # while True:
        #
        #     if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
        #         break
        #     else:
        #         print("\tIP地址无效，请重新输入")
        #         continue
        return ip

    # 建立adb连接
    def _connect(self):
        os.system('adb kill-server')
        os.system('adb connect {}'.format(self.ip))

    # 检查连接状态是否为"device"
    def _connect_status_check(self):
        while True:
            try:
                result = os.popen('adb get-state').readlines()
                if 'device' in result[0]:
                    print("\t已正确连接至TV端")
                    break
                else:
                    print("\t连接状态异常，正在尝试重新连接...")
                    self._connect()
                    continue
            except IndexError:
                print("\t连接状态异常，正在尝试重新连接...")
                self._connect()
                continue

    # adb连接主函数
    def connect(self):
        self._connect()
        # os.popen('adb root')
        # os.popen('adb remount')
        self._connect_status_check()


if __name__ == '__main__':
    connector = ConnectTv()
    connector.connect()
