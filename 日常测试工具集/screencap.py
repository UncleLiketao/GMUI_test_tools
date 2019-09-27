import os
import datetime
import connect_tv



def screencap():
    now = datetime.datetime.now().strftime('%m-%d-%H-%M-%S')
    os.system('adb shell screencap -p /sdcard/sc.png')
    if not os.path.exists('D:\BUG截图'):
        os.mkdir('D:\BUG截图')
    else:
        os.system('adb pull /sdcard/sc.png D:\BUG截图\sc-{}.png'.format(now))


# connect_tv = connect_tv.ConnectTv()
# connect_tv.connect()
screencap()
