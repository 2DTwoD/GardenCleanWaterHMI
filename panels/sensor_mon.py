
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

from misc import di
from misc.own_types import getGeometryStep
from misc.updater import Updater


class SensorMon(QLabel, Updater):
    def __init__(self, labelText, position: QPoint):
        super().__init__(labelText)
        self.colors = ['#C0C0C0', '#00FF00']
        self.labelText = labelText
        self.periphValues = di.Container.periphValues()
        self.setParent(di.Container.mainWindow())
        self.setGeometry(0, 0, int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()))
        self.setFont(QFont('Times', 16))
        self.move(position.x(), position.y())
        self.setBackColor(0)
        self.startUpdate()

    def setBackColor(self, index):
        self.setStyleSheet(f"background: {self.colors[index > 0]}; color: white")

    def updateAction(self):
        self.setBackColor(self.periphValues.getValue(self.labelText))
