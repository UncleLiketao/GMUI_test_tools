import pickle
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def writeSum(init, data=None, path="data.pickle"):
    if init == 0:
        result = data
    else:
        _read = readInfo(path)
        result = _read - 1

    with open(path, 'wb') as f:
        print("------writeSum-------")
        print(result)
        pickle.dump(result, f)


def readSum(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError:
            data = {}
            print("读取文件错误")
    print("------read-------")
    print(path)
    print(data)
    return data


def readInfo(path):
    with open(path, 'rb') as f:
        try:
            data = pickle.load(f)
            # print(data)
        except EOFError:
            data = []
            # print("读取文件错误")
    print("------read-------")
    print(path)
    print(data)
    return data


def writeInfo(data, path="data.pickle"):
    _read = readInfo(path)
    result = []
    if _read:
        _read.append(data)
        result = _read
    else:
        result.append(data)
    with open(path, 'wb') as f:
        print("------writeInfo-------")
        print(result)
        pickle.dump(result, f)


if __name__ == "__main__":
    # readInfo(PATH("../info/192.168.36.108_battery.pickle"))
    # readInfo(PATH("../info/192.168.36.108_fps.pickle"))
    # readInfo(PATH("../info/192.168.36.108_battery.pickle"))
    # readInfo(PATH("../info/192.168.36.108_men.pickle"))
    # readInfo(PATH("../info/192.168.36.108_men.pickle"))
    # readInfo(PATH("../info/192.168.36.108_cpu.pickle"))
    readInfo(PATH("../info/info.pickle"))
