from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from misc import di
from misc.own_types import getGeometryStep


class MousePos(QWidget):
    def __init__(self, enable=False):
        super().__init__()

        self.setParent(di.Container.mainWindow())

        self.pos = QPoint(0, 0)
        self.globPos = QPoint(0, 0)

        self.box = QVBoxLayout()
        self.xPosLabel = QLabel("0")
        self.xPosLabel.setFixedSize(getGeometryStep() * 10, getGeometryStep() * 3)
        self.yPosLabel = QLabel("0")
        self.yPosLabel.setFixedSize(getGeometryStep() * 10, getGeometryStep() * 3)
        self.box.addWidget(self.xPosLabel)
        self.box.addWidget(self.yPosLabel)
        if enable:
            self.setLayout(self.box)

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


