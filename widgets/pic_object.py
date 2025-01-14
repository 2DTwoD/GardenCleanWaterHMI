import threading

from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QLabel

from misc import di
from misc.own_types import ObjectType, RotateDir


class PicObject(QLabel):
    def __init__(self, labelText, parent=None, objectType=ObjectType.PUMP, rotation=RotateDir.RIGHT):
        super(QLabel, self).__init__()
        self.periphValues = di.Container.periphValues()
        self.labelText = labelText

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
        self.timer = None
        self.startUpdate()

    def switchPic(self, picPathIndex=0):
        self.pixmap = QPixmap(self.picPathList[picPathIndex > 0])
        self.pixmap = self.pixmap.transformed(self.transform)
        self.setPixmap(self.pixmap)

    def startUpdate(self):
        self.switchPic(self.periphValues.getValue(self.labelText))
        print(self.labelText)
        self.timer = threading.Timer(1, self.startUpdate)
        self.timer.start()

