from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

from misc import di
from misc.own_types import getGeometryStep


class SensorMon(QLabel):
    def __init__(self, labelText, position: QPoint):
        super(SensorMon, self).__init__(labelText)
        self.colors = ['lightgray', 'lightgreen']
        self.setParent(di.Container.mainWindow())
        self.setGeometry(0, 0, int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()))
        self.setFont(QFont('Times', 16))
        self.move(position.x(), position.y())
        self.setBackColor(0)

    def setBackColor(self, index):
        self.setStyleSheet(f"background: {self.colors[index > 0]}; color: white")

