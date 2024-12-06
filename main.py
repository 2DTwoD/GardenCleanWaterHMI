import sys
from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform, QFont, QPainter, QPen, QColor, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton

geometryStep = 10


class RotateDir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class ObjectType(Enum):
    PUMP = 0
    VALVE = 1

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MousePos(QWidget):
    def __init__(self, parent):
        super(MousePos, self).__init__()
        self.setParent(parent)
        self.xPos = QLabel("0", parent=self)
        self.xPos.setGeometry(0, 0, geometryStep * 10, geometryStep * 2)
        self.yPos = QLabel("0", parent=self)
        self.yPos.setGeometry(0, self.xPos.geometry().height(), geometryStep * 10, geometryStep * 2)
        self.setMouseTracking(True)
        self.xPos.setMouseTracking(True)
        self.yPos.setMouseTracking(True)

    def updatePos(self, x, y):
        self.xPos.setText(f'X: {x}')
        self.yPos.setText(f'Y: {y}')


class Item(QWidget):
    def __init__(self, parent, labelText, type: ObjectType, position: Point, rotation: RotateDir):
        super(Item, self).__init__()
        self.setParent(parent)
        self.setFixedSize(8 * geometryStep, 5 * geometryStep)
        label = QLabel(labelText, parent=self)
        labX = int(1.5 * geometryStep) if type == ObjectType.VALVE and rotation.value % 2 == 1 else 0
        label.setGeometry(labX, 0, 3 * geometryStep, 2 * geometryStep)
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
        picture.setGeometry(3 * geometryStep, 0, 50, 50)
        self.setMouseTracking(True)
        self.move(position.x - int(5.5 * geometryStep), position.y - int(2.5 * geometryStep))


class SensorMon(QWidget):
    def __init__(self, parent, labelText, position: Point):
        super(SensorMon, self).__init__()
        label = QLabel(labelText, parent=self)
        label.setFont(QFont('Times', 16))
        label.setStyleSheet("background: transparent; color: white")
        self.setParent(parent)
        self.move(position.x, position.y)
        self.wid = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor('lightgray'))
        brush = QBrush()
        brush.setColor(QColor("lightgray"))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(0, 0, int(2.5 * geometryStep), int(2.5 * geometryStep) + self.wid)
        painter.end()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Очистка воды HMI")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background: white; background-image: url(pics/back.png)")
        self.M1 = Item(self, "M1", ObjectType.PUMP, Point(265, 185), RotateDir.LEFT)
        self.M2 = Item(self, "M2", ObjectType.PUMP, Point(495, 187), RotateDir.LEFT)
        self.M3 = Item(self, "M3", ObjectType.PUMP, Point(723, 187), RotateDir.LEFT)
        self.M7 = Item(self, "M7", ObjectType.PUMP, Point(804, 542), RotateDir.RIGHT)
        self.C1 = Item(self, "C1", ObjectType.VALVE, Point(185, 90), RotateDir.DOWN)
        self.C2 = Item(self, "C2", ObjectType.VALVE, Point(410, 90), RotateDir.DOWN)
        self.C3 = Item(self, "C3", ObjectType.VALVE, Point(639, 90), RotateDir.DOWN)
        self.D1 = Item(self, "D1", ObjectType.VALVE, Point(106, 390), RotateDir.DOWN)
        self.D2 = Item(self, "D2", ObjectType.VALVE, Point(336, 390), RotateDir.DOWN)
        self.D3 = Item(self, "D3", ObjectType.VALVE, Point(563, 390), RotateDir.DOWN)
        self.D4 = Item(self, "D4", ObjectType.VALVE, Point(680, 580), RotateDir.LEFT)
        self.O1 = Item(self, "O1", ObjectType.VALVE, Point(276, 465), RotateDir.DOWN)
        self.O2 = Item(self, "O2", ObjectType.VALVE, Point(502, 465), RotateDir.DOWN)
        self.O3 = Item(self, "O3", ObjectType.VALVE, Point(730, 465), RotateDir.DOWN)
        self.B1 = SensorMon(self, "B1", Point(228, 240))
        # self.but = QPushButton("херачь!", parent=self)
        # self.but.released.connect(lambda: self.the_button_was_clicked(self.sens))
        # self.but.move(800, 300)
        self.setMouseTracking(True)
        self.mousePos = MousePos(self)
        self.show()

    # def the_button_was_clicked(self, sens):
    #     sens.wid += 1
    #     sens.update()

    def mouseMoveEvent(self, event):
        try:
            self.mousePos.updatePos(event.pos().x(), event.pos().y())
        except Exception as msg:
            print('Error with mouse move: ' + str(msg))


app = QApplication(sys.argv)
window = MainWindow()
app.exec()
