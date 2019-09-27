import math


def avgMen(men, total):
    """
    计算内存均值
    :param men:
    :param total: rom容量
    :return:
    """
    if len(men):
        _men = [math.ceil(((men[i]) / total) * 1024) for i in range(len(men))]
        print(_men)
        return str(math.ceil(sum(_men) / len(_men))) + "M"
    return "0"


def avgCpu(cpu):
    """
    计算cpu均值
    :param cpu:
    :return:
    """
    if len(cpu):
        resutl = "%.1f" % (sum(cpu) / len(cpu))
        return str(math.ceil(float(resutl) * 10)) + "%"
    return "0%"


def avgFps(fps):
    """
    计算FPS均值
    :param fps:
    :return:
    """
    if len(fps):
        return '%.2f' % float(str(math.ceil(sum(fps) / len(fps))))
    return 0.00


def maxMen(men):
    """
    计算内存峰值
    :param men:
    :return:
    """
    if len(men):
        print("men=" + str(men))
        return str(math.ceil((max(men)) / 1024)) + "M"
    return "0M"


def maxCpu(cpu):
    """
    计算Cpu使用峰值
    :param cpu:
    :return:
    """
    print("maxCpu=" + str(cpu))
    if len(cpu):
        result = "%.1f" % max(cpu)
        return str(math.ceil(float(result) * 10)) + "%"
    return "0%"


def maxFps(fps):
    """
    计算FPS峰值
    :param fps:
    :return:
    """
    return str(max(fps))


if __name__ == '__main__':
    cpu = [1.9164759725400458, 0.40045766590389015, 0.8493771234428086, 1.8407534246575343]
    men = [310171, 323267, 321179, 317913, 316569, 335277, 323853, 315837, 333765, 333829, 337433, 337473, 339877,
           328953, 328881, 328909, 334029, 329873, 334645, 338649, 332541, 329273, 333581]

    print(avgMen(men, 3014000))

