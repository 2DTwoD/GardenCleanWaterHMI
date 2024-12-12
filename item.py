from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QGridLayout

from items.picObject import PicObject
from own_types import ObjectType, RotateDir, getGeometryStep
import di as DI


class ControlWindow(QWidget):
    def __init__(self, labelText, objectType: ObjectType):
        super(ControlWindow, self).__init__()
        self.buttonTextList = ["Старт " + labelText, "Стоп " + labelText]
        if objectType == ObjectType.VALVE:
            self.buttonTextList = ["Открыть " + labelText, "Закрыть " + labelText]
        self.mousePos = DI.Container.mousePos()
        self.setWindowTitle(labelText)
        self.setGeometry(self.mousePos.getGlobalPos().x(), self.mousePos.getGlobalPos().y(), 200, 100)
        self.picObject = PicObject(objectType=objectType)
        self.on = QPushButton(self.buttonTextList[0])
        self.off = QPushButton(self.buttonTextList[1])
        self.grid = QGridLayout()
        self.grid.addWidget(self.picObject, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.on, 1, 0)
        self.grid.addWidget(self.off, 1, 1)
        self.setLayout(self.grid)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)
        self.setFixedSize(200, 100)


class Item(QWidget):
    controlWindow: ControlWindow = None

    def __init__(self, text, objectType: ObjectType, position: QPoint, rotation: RotateDir):
        super(Item, self).__init__()
        self.objectType = objectType
        self.setParent(DI.Container.mainWindow())
        self.setFixedSize(8 * getGeometryStep(), 5 * getGeometryStep())
        self.labelText = text
        self.position = position
        self.label = QLabel(text, parent=self)
        labX = int(1.5 * getGeometryStep()) if objectType == ObjectType.VALVE and rotation.value % 2 == 1 else 0
        self.label.setGeometry(labX, 0, 3 * getGeometryStep(), 2 * getGeometryStep())
        self.label.setFont(QFont('Times', 16))
        self.label.setStyleSheet("background: transparent;")
        self.picObject = PicObject(parent=self, objectType=objectType, rotation=rotation)
        self.picObject.setGeometry(3 * getGeometryStep(), 0,
                                   self.picObject.geometry().width(), self.picObject.geometry().height())
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.move(position.x() - int(5.5 * getGeometryStep()), position.y() - int(2.5 * getGeometryStep()))

    def mouseReleaseEvent(self, e):
        self.controlWindow = ControlWindow(self.labelText, self.objectType)
        self.controlWindow.show()
        self.picObject.switchPic(1)
