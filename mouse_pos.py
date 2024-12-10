from PyQt6.QtWidgets import QWidget, QLabel

from own_types import getGeometryStep


class MousePos(QWidget):
    def __init__(self, parent):
        super(MousePos, self).__init__()
        self.setGeometry(0, 0, 100, 40)
        self.setParent(parent)
        self.xPos = QLabel("0", parent=self)
        self.xPos.setGeometry(0, 0, getGeometryStep() * 10, getGeometryStep() * 2)
        self.yPos = QLabel("0", parent=self)
        self.yPos.setGeometry(0, self.xPos.geometry().height(), getGeometryStep() * 10, getGeometryStep() * 2)
        self.setMouseTracking(True)
        self.xPos.setMouseTracking(True)
        self.yPos.setMouseTracking(True)

    def updatePos(self, x, y):
        self.xPos.setText(f'X: {x}')
        self.yPos.setText(f'Y: {y}')

