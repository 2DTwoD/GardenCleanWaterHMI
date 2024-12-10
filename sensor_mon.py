from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush
from PyQt6.QtWidgets import QWidget, QLabel

from own_types import Point, getGeometryStep


class SensorMon(QWidget):
    def __init__(self, parent, labelText, position: Point):
        super(SensorMon, self).__init__()
        self.setGeometry(0, 0, int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()))
        label = QLabel(labelText, parent=self)
        label.setFont(QFont('Times', 16))
        label.setStyleSheet("background: transparent; color: white")
        self.setParent(parent)
        self.move(position.x, position.y)
        self.wid = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor('lightgray'))
        brush = QBrush()
        brush.setColor(QColor("lightgray"))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(0, 0, int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()) + self.wid)
        painter.end()

