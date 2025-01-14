import json
import threading

from misc.own_types import TankNumber


class CommonDict(dict):
    lock = threading.Lock()

    def __init__(self):
        super(dict, self).__init__()

    def updateValues(self, jsonString):
        try:
            newValues = json.loads(jsonString)
        except ValueError:
            print('Ошибка в JSON')
            return
        with self.lock:
            if sorted(self.keys()) == sorted(newValues.keys()):
                self.update(newValues)

    def getValue(self, key):
        with self.lock:
            return self[key]


class PeriphValues(CommonDict):
    def __init__(self):
        super(CommonDict, self).__init__()
        self.__setitem__("H1", 0)
        self.__setitem__("H2", 0)
        self.__setitem__("H3", 0)
        self.__setitem__("B1", 0)
        self.__setitem__("B2", 0)
        self.__setitem__("B3", 0)
        self.__setitem__("S4", 0)
        self.__setitem__("S5", 0)
        self.__setitem__("S6", 0)
        self.__setitem__("C1", 0)
        self.__setitem__("C2", 0)
        self.__setitem__("C3", 0)
        self.__setitem__("O1", 0)
        self.__setitem__("O2", 0)
        self.__setitem__("O3", 0)
        self.__setitem__("D1", 0)
        self.__setitem__("D2", 0)
        self.__setitem__("D3", 0)
        self.__setitem__("D4", 0)
        self.__setitem__("M1", 0)
        self.__setitem__("M2", 0)
        self.__setitem__("M3", 0)
        self.__setitem__("M6", 0)
        self.__setitem__("M7", 0)


class OBvalues(CommonDict):
    def __init__(self):
        super(CommonDict, self).__init__()
        self.__setitem__("step", 0)
        self.__setitem__("auto", 0)
        self.__setitem__("s1St", 0)
        self.__setitem__("s2St", 0)
        self.__setitem__("s3St", 0)
        self.__setitem__("s4St", 0)
        self.__setitem__("s5St", 0)
        self.__setitem__("s6St", 0)
        self.__setitem__("s2Per", 0)
        self.__setitem__("s2TimeRem", 0)
        self.__setitem__("s3Per", 0)
        self.__setitem__("s3TimeRem", 0)
        self.__setitem__("s4Per", 0)
        self.__setitem__("s4TimeRem", 0)
        self.__setitem__("s5Per", 0)
        self.__setitem__("s5TimeRem", 0)


class CHBvalues(CommonDict):
    def __init__(self):
        super(CommonDict, self).__init__()
        self.__setitem__("step", 0)
        self.__setitem__("auto", 0)
        self.__setitem__("s1St", 0)
        self.__setitem__("s2St", 0)
        self.__setitem__("s3St", 0)
        self.__setitem__("s2Per", 0)
        self.__setitem__("s2TimeRem", 0)
        self.__setitem__("queue", "000")


class TankValues(list):
    def __init__(self):
        super(list, self).__init__()
        self.append(CHBvalues())
        self.append(OBvalues())
        self.append(OBvalues())
        self.append(OBvalues())

    def select(self, tankNumber: TankNumber):
        return self[tankNumber.value]

    def get(self, tankNumber: TankNumber, key):
        return self[tankNumber.value].getValue(key)
