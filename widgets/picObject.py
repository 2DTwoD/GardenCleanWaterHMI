from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QLabel

from misc.own_types import ObjectType, RotateDir


class PicObject(QLabel):
    def __init__(self, parent=None, objectType=ObjectType.PUMP, rotation=RotateDir.RIGHT):
        super(PicObject, self).__init__()
        self.setParent(parent)
        self.pixmap = None
        self.transform = QTransform()
        self.transform.rotate(90 * rotation.value)
        self.picPathList = ['pics/pump_stopped.png', 'pics/pump_started.png']
        if objectType == ObjectType.VALVE:
            self.picPathList = ['pics/valve_closed.png', 'pics/valve_opened.png']
        self.setStyleSheet("background: transparent;")
        self.switchPic()
        self.setGeometry(0, 0, 50, 50)
        self.setMouseTracking(True)

    def switchPic(self, picPathIndex=0):
        self.pixmap = QPixmap(self.picPathList[picPathIndex > 0])
        self.pixmap = self.pixmap.transformed(self.transform)
        self.setPixmap(self.pixmap)
