from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout

from misc import di
from misc.updater import Updater
from widgets.brics import SButton, SLabel
from widgets.pic_object import PicObject
from misc.own_types import ObjectType, RotateDir, getGeometryStep, TankNumber

autoList = ["Р", "А"]
autoColorList = ["orange", "#00FF00"]

class AutoIcon(SLabel):
    def __init__(self, tankNumber: TankNumber, parent=None):
        super().__init__(autoList[0], parent=parent, size=16, transparent=True, color=autoColorList[0], bold=True)
        self.tankNumber = tankNumber
        self.tankValues = di.Container.tankValues()

    def updateVis(self):
        self.setText(autoList[self.tankValues.get(self.tankNumber, "auto")])
        self.setColor(autoColorList[self.tankValues.get(self.tankNumber, "auto")])

class ControlWindow(QWidget, Updater):
    def __init__(self, labelText, objectType: ObjectType, tankNumber: TankNumber):
        super().__init__()

        self.periphValues = di.Container.periphValues()
        self.tankValues = di.Container.tankValues()
        self.comm = di.Container.comm()
        mousePos = di.Container.mousePos()
        self.labelText = labelText
        self.tankNumber = tankNumber

        if objectType == ObjectType.VALVE:
            self.buttonTextList = ["Открыть " + labelText, "Закрыть " + labelText]
            self.setWindowIcon(QIcon('pics/icons/valve.png'))
        else:
            self.buttonTextList = ["Старт " + labelText, "Стоп " + labelText]
            self.setWindowIcon(QIcon('pics/icons/pump.png'))

        self.setWindowTitle(labelText)
        self.move(mousePos.getGlobalPos().x(), mousePos.getGlobalPos().y())
        self.setFixedSize(20 * getGeometryStep(), 14 * getGeometryStep())

        self.picObject = PicObject(objectType=objectType)
        self.autoIcon = AutoIcon(tankNumber)
        self.on = SButton(self.buttonTextList[0])
        self.off = SButton(self.buttonTextList[1])
        self.grid = QGridLayout()
        self.grid.addWidget(self.picObject, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.autoIcon, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.on, 2, 0)
        self.grid.addWidget(self.off, 2, 1)

        self.setLayout(self.grid)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)

        self.on.clicked.connect(lambda: self.onOffButtonClick(1))
        self.off.clicked.connect(lambda: self.onOffButtonClick(0))
        self.startUpdate()

    def onOffButtonClick(self, value):
        if self.tankValues.get(self.tankNumber, "auto") == 0:
            self.comm.send(f"[set.{self.labelText.lower()}.{value}]")

    def updateAction(self):
        self.picObject.switchPic(self.periphValues.getValue(self.labelText))
        self.autoIcon.updateVis()

    def closeEvent(self, event):
        self.stopUpdate()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape.value:
            self.close()

class Item(QWidget, Updater):

    def __init__(self, labelText, objectType: ObjectType, position: QPoint, rotation: RotateDir, tankNumber: TankNumber):
        super().__init__(parent=di.Container.mainWindow())

        self.objectType = objectType
        self.periphValues = di.Container.periphValues()
        self.tankValues = di.Container.tankValues()
        self.labelText = labelText
        self.tankNumber = tankNumber
        self.controlWindow = None
        labX = int(1.5 * getGeometryStep()) if objectType == ObjectType.VALVE and rotation.value % 2 == 1 else 0
        shiftAutIcon = getGeometryStep() if objectType == ObjectType.VALVE and rotation.value % 2 == 1 else 0

        self.setFixedSize(12 * getGeometryStep(), 5 * getGeometryStep())

        self.label = SLabel(labelText, parent=self, size=16, transparent=True)
        self.label.setGeometry(labX, 0, 3 * getGeometryStep(), int(2.2 * getGeometryStep()))
        self.picObject = PicObject(parent=self, objectType=objectType, rotation=rotation)
        self.picObject.move(3 * getGeometryStep(), 0)
        self.autoIcon = AutoIcon(tankNumber, parent=self)
        self.autoIcon.move(self.label.width() + self.picObject.width() - shiftAutIcon, 0)

        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.autoIcon.setMouseTracking(True)
        self.move(position.x() - int(5.5 * getGeometryStep()), position.y() - int(2.5 * getGeometryStep()))

        self.startUpdate()

    def mouseReleaseEvent(self, e):
        if self.controlWindow is not None:
            self.controlWindow.close()
        self.controlWindow = ControlWindow(self.labelText, self.objectType, self.tankNumber)
        self.controlWindow.show()

    def updateAction(self):
        self.picObject.switchPic(self.periphValues.getValue(self.labelText))
        self.autoIcon.updateVis()
