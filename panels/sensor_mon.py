from PyQt6.QtCore import QPoint

from misc import di
from misc.own_types import getGeometryStep
from misc.updater import Updater
from widgets.brics import SLabel

sensorColors = ['#C0C0C0', '#00FF00']

class SensorMon(SLabel, Updater):
    def __init__(self, labelText, position: QPoint):
        super().__init__(labelText, parent=di.Container.mainWindow(), size=16)

        self.periphValues = di.Container.periphValues()
        self.labelText = labelText

        self.setFixedSize(int(2.5 * getGeometryStep()), int(2.5 * getGeometryStep()))
        self.move(position.x(), position.y())

        self.startUpdate()

    def updateAction(self):
        self.setStyleSheet(f"background: {sensorColors[self.periphValues.getValue(self.labelText) > 0]}; color: white")
