from enum import Enum


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