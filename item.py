from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton

from items.picObject import PicObject
from own_types import ObjectType, RotateDir, getGeometryStep
import di as DI


class ControlWindow(QWidget):
    def __init__(self, labelText):
        super(ControlWindow, self).__init__()
        self.mousePos = DI.Container.mousePos()
        self.setWindowTitle(labelText)
        self.setGeometry(self.mousePos.getGlobalPos().x(), self.mousePos.getGlobalPos().y(), 200, 100)
        layout = QHBoxLayout()
        self.label = QLabel(labelText)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)


class Item(QWidget):
    controlWindow: ControlWindow = None

    def __init__(self, text, type: ObjectType, position: QPoint, rotation: RotateDir):
        super(Item, self).__init__()
        self.setParent(DI.Container.mainWindow())
        self.setFixedSize(8 * getGeometryStep(), 5 * getGeometryStep())
        self.labelText = text
        self.position = position
        self.hBoxLayout = QHBoxLayout()
        self.on = QPushButton(text)
        self.off = QPushButton(text)
        self.hBoxLayout.addWidget(self.on)
        self.hBoxLayout.addWidget(self.off)
        self.setLayout(self.hBoxLayout)
        # labX = int(1.5 * getGeometryStep()) if type == ObjectType.VALVE and rotation.value % 2 == 1 else 0
        label.setGeometry(labX, 0, 3 * getGeometryStep(), 2 * getGeometryStep())
        label.setFont(QFont('Times', 16))
        label.setStyleSheet("background: transparent;")
        self.picObject = PicObject(parent=self, type=type, rotation=rotation)
        self.picObject.setGeometry(3 * getGeometryStep(), 0,
                                   self.picObject.geometry().width(), self.picObject.geometry().height())
        self.setMouseTracking(True)
        label.setMouseTracking(True)
        self.move(position.x() - int(5.5 * getGeometryStep()), position.y() - int(2.5 * getGeometryStep()))

    def mouseReleaseEvent(self, e):
        self.controlWindow = ControlWindow(self.labelText)
        self.controlWindow.show()
        self.picObject.switchPic(1)
