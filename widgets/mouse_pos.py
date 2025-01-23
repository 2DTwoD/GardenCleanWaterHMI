from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget, QLabel

from misc import di
from misc.own_types import getGeometryStep


class MousePos(QWidget):
    def __init__(self):
        super().__init__(parent=di.Container.mainWindow())

        self.pos = QPoint(0, 0)
        self.globPos = QPoint(0, 0)

        self.xPosLabel = QLabel("0", parent=self)
        self.xPosLabel.setGeometry(0, 0, getGeometryStep() * 10, getGeometryStep() * 2)
        self.yPosLabel = QLabel("0", parent=self)
        self.yPosLabel.setGeometry(0, self.xPosLabel.height(), getGeometryStep() * 10, getGeometryStep() * 2)

        self.setMouseTracking(True)
        self.xPosLabel.setMouseTracking(True)
        self.yPosLabel.setMouseTracking(True)
        self.setGeometry(0, 0, self.xPosLabel.width(), self.xPosLabel.height() + self.yPosLabel.height())

    def updatePos(self, x, y):
        self.pos.setX(x)
        self.pos.setY(y)
        self.globPos = self.mapToGlobal(self.pos)
        self.xPosLabel.setText(f'X: {x}')
        self.yPosLabel.setText(f'Y: {y}')

    def getPos(self):
        return self.pos

    def getGlobalPos(self):
        return self.globPos


