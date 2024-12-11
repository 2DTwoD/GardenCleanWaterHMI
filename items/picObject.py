from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QWidget, QLabel

from own_types import ObjectType, RotateDir


class PicObject(QWidget):
    def __init__(self, parent=None, type=ObjectType.PUMP, rotation=RotateDir.RIGHT):
        super(PicObject, self).__init__()
        self.setParent(parent)
        self.picture = QLabel(parent=self)
        self.pixmap = None
        self.transform = QTransform()
        self.transform.rotate(90 * rotation.value)
        if type == ObjectType.PUMP:
            self.picPathList = ['pics/pump_stopped.png', 'pics/pump_started.png']
        else:
            self.picPathList = ['pics/valve_closed.png', 'pics/valve_opened.png']
        self.picture.setStyleSheet("background: transparent;")
        self.switchPic()
        self.picture.setGeometry(0, 0, 50, 50)
        self.setMouseTracking(True)
        self.picture.setMouseTracking(True)

    def switchPic(self, picPathIndex=0):
        self.pixmap = QPixmap(self.picPathList[picPathIndex])
        self.pixmap = self.pixmap.transformed(self.transform)
        self.picture.setPixmap(self.pixmap)

