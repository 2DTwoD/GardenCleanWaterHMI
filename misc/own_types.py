from enum import Enum


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


def getGeometryStep():
    return 10

