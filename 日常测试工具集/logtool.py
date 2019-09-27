import os
import datetime
import connect_tv


def get_log():
    if not os.path.exists('D:\BUG日志'):
        os.mkdir('D:\BUG日志')
    logfile = 'D:\BUG日志\{}'.format(now)
    os.mkdir(logfile)
    # os.mkdir(logfile+'\\tombstones')
    # 拷贝AppError
    # print('\t开始拷贝AppError.txt...')
    # os.system('adb pull /data/appError.txt {}'.format(logfile))
    # print('拷贝进程结束\n')
    # 拷贝syslog
    print('\t开始拷贝syslog...')
    os.system('adb pull /sdcard/syslog/logcat.log {}'.format(logfile))
    print('拷贝进程结束\n')
    # 拷贝old_syslog
    # print('\t开始拷贝oldsyslog...')
    # os.system('adb pull /sdcard/syslog/old_logcat.log {}'.format(logfile))
    # print('拷贝进程结束\n')
    # 拷贝anr下traces.txt
    # print('\t开始拷贝anr下的文件...')
    # os.system('adb pull /data/anr/traces.txt {}'.format(logfile))
    # print('拷贝进程结束\n')
    # 拷贝tombstones目录下所有文件
    # print('\t开始拷贝tombstones下的文件...')
    # os.system('adb pull /data/tombstones {}'.format(logfile))
    # print('拷贝进程结束\n')
    # 拷贝hci log
    # print('\t开始拷贝hci log...')
    # os.system('adb pull /data/misc/bluedroid/btsnoop_hci.log {}'.format(logfile))


now = datetime.datetime.now().strftime('%b-%d-%Y-%H-%M-%S')
connect_tv = connect_tv.ConnectTv()
connect_tv.connect()
get_log()
