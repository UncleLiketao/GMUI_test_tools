"""
GMUI版本验证工具
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import time
import connect_tv
import logging
logging.basicConfig(level=logging.INFO)

package_list = {'XgimiUiApi': 'com.xgimiui.api', 'XgimiDatareporter': 'com.xgimi.datareporter',
                'XgimiPaySdk': 'com.xgimi.payview', 'XgimiBootwizard': 'com.xgimi.bootwizard',
                'XgimiHome': 'com.xgimi.home', 'XgimiInstrucation': 'com.xgimi.instruction30',
                'XgimiManager': 'com.xgimi.manager', 'XgimiMediaPlayer': 'com.xgimi.gimiplayer',
                'XgimiMisckey': 'com.xgimi.misckey', 'XgimiMsgcenter': 'com.xgimi.msgcenter',
                'XgimiWeather': 'com.xgimi.weather',  'XgimiMusicPlayer': 'com.xgimi.doubanfm',
                'XgimiResManager': 'com.xgimi.filemanager', 'XgimiSetting': 'com.android.newsettings',
                'XgimiSystwind': 'com.xgimi.windowsystem', 'XgimiTheme': 'com.xgimi.theme',
                'XgimiUpdate': 'com.xgimi.upgrade', 'XgimiUser': 'com.xgimi.user', 'XgimiVoice': 'com.xgimi.duertts',
                'XgimiVoiceOffline': 'com.xgimi.voiceoffline', 'XgimiAppDb': 'com.xgimi.appdb',
                'XgimiAppMarket': 'com.xgimi.appmarket',
                'XgimiWirelessscreen': 'com.xgimi.wirelessscreen', 'XgimiVcontrol': 'com.xgimi.vcontrol',
                'XgimiJOS': 'com.jd.smart.tv.sdk', 'XgimiScreenSaver': 'com.xgimi.screensaver',
                'XgimiStreamPlayer': 'com.xgimi.streammeadiaplayer',
                'XgimiAdService': 'com.xgimi.adservice', 'HunanOTT': 'com.hunantv.license',
                'QiyiVideo': 'com.gitvjimi.video', 'MangoGame卸': 'com.mango.game.mangotvgame',
                'SogouIME': 'com.sohu.inputmethod.sogou.tv', 'WPS卸': 'cn.wps.moffice_i18n_TV',
                'TVSports卸': 'com.pptv.tvsports', 'Qibabu': 'com.gitvchild.jimi', 'SohuTV卸': 'com.sohuott.tv.vod',
                'QQMusic': 'hk.reco.qqmusic', 'TencentTVLite': 'com.ktcp.tvvideo', 'TencentTV': 'com.ktcp.tvvideo',
                'XgimiArtMode': 'com.xgimi.artmode'
                }

correct_versions = {}
current_versions = {}


# 与测试设备建立adb连接

connector = connect_tv.ConnectTv()
connector.connect()


# 处理版本号

def get_version_name(version_name):
    right_version_name = version_name
    if str(version_name).upper().startswith("NEW_V"):
        right_version_name = version_name[5:]
    if str(version_name).upper().startswith("V"):
        right_version_name = version_name[1:]
    if str(version_name).upper().startswith("RELEASE_V"):
        right_version_name = version_name[9:]
    if str(right_version_name).find("_") != -1:
        right_version_name = str(right_version_name)[:str(right_version_name).find("_")]
    return right_version_name


# 生成CMD命令

def gen_command(package="com.android.newsettings"):
    return "adb shell dumpsys package " + str(package)


# 执行CMD命令并且返回版本号

def exec_command(command):
    result = os.popen(command)
    lines = result.readlines()
    for line in lines:
        if line.strip().startswith("versionName"):
            version_line = line.split("=")
            version_name = version_line[-1]
            return version_name


# 获取当前的所有版本号

def get_versions():
    global current_versions
    logging.info("正在获取TV端版本信息......")
    for key, value in package_list.items():
        version_name = exec_command(gen_command(value))
        current_versions[key] = get_version_name(str(version_name).rstrip())


# 爬取XGIMI-GMUI版本中心的正确版本号

def right_version():
    global correct_versions
    GMUI_VERSION = input("请输入GMUI版本号：")
    PLANTFORM = input("请输入搭载平台：")
    driver = webdriver.Chrome()
    driver.get("http://gmui-version.xgimi-dev.com/VersionCenter.php")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "GMUIVersionList"))
    )
    time.sleep(5)
    Select(driver.find_element_by_id('GMUIVersionList')).select_by_value(GMUI_VERSION)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "TVList"))
    )
    time.sleep(10)
    Select(driver.find_element_by_id("TVList")).select_by_visible_text(PLANTFORM)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "QueryButton"))
    )
    driver.find_element_by_id("QueryButton").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='AppInfoContent']/p[1]/span"))
    )
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id="LogCommitTable")

    LogCommitTable = []
    for tr in table.find_all('tr'):
        for td in tr.find_all('td'):
            LogCommitTable.append(td.get_text())
    name_index_list = list(filter(lambda x: x % 10 == 0, range(0, len(LogCommitTable))))
    version_index_list = list(filter(lambda x: x % 10 == 5, range(0, len(LogCommitTable))))
    name_list = []
    verison_list = []
    for i in name_index_list:
        name_list.append(LogCommitTable[i])
    for i in version_index_list:
        verison_list.append(get_version_name(LogCommitTable[i]))
    correct_versions = dict(zip(name_list, verison_list))


def cmp_versions():
    """对比版本号"""
    get_versions()
    right_version()
    faild_list = []
    not_found_list = []
    count_success = 0
    for i in correct_versions:
        try:
            if not correct_versions[i] == current_versions[i]:
                print("包名：" + str(i) + "测试失败")
                print("当前的版本为：" + current_versions[i])
                print("正确的版本为：" + correct_versions[i])
                faild_list.append(i)
            else:
                count_success += 1
        except KeyError:
            print("找不到包:" + str(i))
            not_found_list.append(i)
    print("检测完成！")
    if len(faild_list) > 0:
        print("检测失败的个数为：" + str(len(faild_list)) + " 分别为：")
        print(faild_list)
    else:
        print("无检测失败的包！")
    print("检测成功的个数为：" + str(count_success))
    if len(not_found_list) > 0:
        print("未找到的个数为：" + str(len(not_found_list)) + " 分别为：")
        print(not_found_list)
    else:
        print("无未找到的包")


cmp_versions()
input("执行完成，请点击任意按键！")