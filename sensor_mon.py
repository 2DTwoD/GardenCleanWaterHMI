from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush
from PyQt6.QtWidgets import QWidget, QLabel

from own_types import getGeometryStep
import di as DI


class SensorMon(QWidget):
    def __init__(self, labelText, position: QPoint):
        super(SensorMon, self).__init__()
        self.setGeometry(0, 0, int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()))
        self.label = QLabel(labelText, parent=self)
        self.label.setFont(QFont('Times', 16))
        self.label.setStyleSheet("background: transparent; color: white")
        self.setParent(DI.Container.mainWindow())
        self.move(position.x(), position.y())
        self.colors = [QColor('lightgray'), QColor('lightgreen')]
        self.pen = QPen()
        self.pen.setWidth(2)
        self.brush = QBrush()
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.label.setMouseTracking(True)
        self.setMouseTracking(True)
        self.colorIndex = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        self.pen.setColor(self.colors[self.colorIndex])
        self.brush.setColor(self.colors[self.colorIndex])
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRect(0, 0, int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()))
        painter.end()

    def setColorIndex(self, index):
        self.colorIndex = index

