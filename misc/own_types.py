from enum import Enum

from PyQt6.QtCore import Qt


class TankNumber(Enum):
    CHB = 0
    OB1 = 1
    OB2 = 2
    OB3 = 3


class ObjectType(Enum):
    PUMP = 0
    VALVE = 1


class RotateDir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class Align(Enum):
    RIGHT = Qt.AlignmentFlag.AlignRight
    LEFT = Qt.AlignmentFlag.AlignLeft
    CENTER = Qt.AlignmentFlag.AlignCenter
    VCENTER = Qt.AlignmentFlag.AlignVCenter


def getGeometryStep():
    return 10

