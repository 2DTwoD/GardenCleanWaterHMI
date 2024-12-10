from PyQt6.QtGui import QPixmap, QTransform, QFont
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout

from own_types import ObjectType, Point, RotateDir, getGeometryStep


class Item(QWidget):
    def __init__(self, parent, labelText, type: ObjectType, position: Point, rotation: RotateDir):
        super(Item, self).__init__()
        self.setParent(parent)
        self.setFixedSize(8 * getGeometryStep(), 5 * getGeometryStep())
        self.labelText = labelText
        self.position = position
        label = QLabel(labelText, parent=self)
        labX = int(1.5 * getGeometryStep()) if type == ObjectType.VALVE and rotation.value % 2 == 1 else 0
        label.setGeometry(labX, 0, 3 * getGeometryStep(), 2 * getGeometryStep())
        label.setFont(QFont('Times', 16))
        label.setStyleSheet("background: transparent;")
        picture = QLabel(parent=self)
        picPath = 'pics/pump_stopped.png' if type == ObjectType.PUMP else 'pics/valve_closed.png'
        pixmap = QPixmap(picPath)
        picture.setStyleSheet("background: transparent;")
        transform = QTransform()
        transform.rotate(90 * rotation.value)
        pixmap = pixmap.transformed(transform)
        picture.setPixmap(pixmap)
        picture.setGeometry(3 * getGeometryStep(), 0, 50, 50)
        self.setMouseTracking(True)
        self.move(position.x - int(5.5 * getGeometryStep()), position.y - int(2.5 * getGeometryStep()))
        # print(self.mapToGlobal())

    def mouseReleaseEvent(self, e):
        self.controlWindow = ControlWindow(self.labelText, self.position)
        self.controlWindow.show()


class ControlWindow(QWidget):
    def __init__(self, labelText, position: Point):
        super(ControlWindow, self).__init__()
        self.setWindowTitle(labelText)
        self.setGeometry(position.x, position.y, 200, 100)
        layout = QHBoxLayout()
        self.label = QLabel(labelText)
        layout.addWidget(self.label)
        self.setLayout(layout)
