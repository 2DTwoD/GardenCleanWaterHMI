from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush
from PyQt6.QtWidgets import QLabel

from own_types import getGeometryStep
import di as DI


class SensorMon(QLabel):
    def __init__(self, labelText, position: QPoint):
        super(SensorMon, self).__init__(labelText)
        self.colors = ['lightgray', 'lightgreen']
        self.setParent(DI.Container.mainWindow())
        self.setGeometry(0, 0, int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()))
        self.setFont(QFont('Times', 16))
        self.move(position.x(), position.y())
        self.setBackColor(0)

    def setBackColor(self, index):
        self.setStyleSheet(f"background: {self.colors[index > 0]}; color: white")

