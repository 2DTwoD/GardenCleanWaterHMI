
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QGridLayout

from misc import di
from misc.updater import Updater
from widgets.brics import SButton, SLabel
from widgets.pic_object import PicObject
from misc.own_types import ObjectType, RotateDir, getGeometryStep


class ControlWindow(QWidget, Updater):
    def __init__(self, labelText, objectType: ObjectType):
        super().__init__()
        self.buttonTextList = ["Старт " + labelText, "Стоп " + labelText]
        self.labelText = labelText
        self.periphValues = di.Container.periphValues()
        self.comm = di.Container.comm()
        if objectType == ObjectType.VALVE:
            self.buttonTextList = ["Открыть " + labelText, "Закрыть " + labelText]
        mousePos = di.Container.mousePos()
        self.setWindowTitle(labelText)
        self.setGeometry(mousePos.getGlobalPos().x(), mousePos.getGlobalPos().y(), 200, 100)
        self.picObject = PicObject(objectType=objectType)
        self.on = SButton(self.buttonTextList[0])
        self.off = SButton(self.buttonTextList[1])
        self.grid = QGridLayout()
        self.grid.addWidget(self.picObject, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.on, 1, 0)
        self.grid.addWidget(self.off, 1, 1)
        self.setLayout(self.grid)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)
        self.setFixedSize(200, 100)
        self.on.clicked.connect(lambda: self.onOffButtonClick(1))
        self.off.clicked.connect(lambda: self.onOffButtonClick(0))
        self.startUpdate()

    def onOffButtonClick(self, value):
        self.comm.send(f"[set.{self.labelText.lower()}.{value}]")

    def updateAction(self):
        self.picObject.switchPic(self.periphValues.getValue(self.labelText))

    def closeEvent(self, event):
        self.stopUpdate()

class Item(QWidget, Updater):
    controlWindow: ControlWindow = None

    def __init__(self, labelText, objectType: ObjectType, position: QPoint, rotation: RotateDir):
        super().__init__()
        self.objectType = objectType
        self.periphValues = di.Container.periphValues()
        self.setParent(di.Container.mainWindow())
        self.setFixedSize(8 * getGeometryStep(), 5 * getGeometryStep())
        self.labelText = labelText
        self.label = SLabel(labelText, parent=self, size=16, transparent=True)
        labX = int(1.5 * getGeometryStep()) if objectType == ObjectType.VALVE and rotation.value % 2 == 1 else 0
        self.label.setGeometry(labX, 0, 3 * getGeometryStep(), int(2.2 * getGeometryStep()))
        self.picObject = PicObject(parent=self, objectType=objectType, rotation=rotation)
        self.picObject.setGeometry(3 * getGeometryStep(), 0,
                                   self.picObject.geometry().width(), self.picObject.geometry().height())
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.move(position.x() - int(5.5 * getGeometryStep()), position.y() - int(2.5 * getGeometryStep()))
        self.startUpdate()

    def mouseReleaseEvent(self, e):
        self.controlWindow = ControlWindow(self.labelText, self.objectType)
        self.controlWindow.show()

    def updateAction(self):
        self.picObject.switchPic(self.periphValues.getValue(self.labelText))
