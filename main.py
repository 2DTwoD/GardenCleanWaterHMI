import sys
from enum import Enum

from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel

geometryStep = 10


class RotateDir(Enum):
    ROT_RIGHT = 0
    ROT_DOWN = 1
    ROT_LEFT = 2
    ROT_UP = 3


class Item(QWidget):
    def __init__(self, parent, labelText, rotation: RotateDir):
        super(Item, self).__init__()
        self.setParent(parent)
        label = QLabel(labelText, parent=self)
        label.setGeometry(0, 0, geometryStep * 2, geometryStep * 2)
        button = QPushButton(labelText, parent=self)
        button.setGeometry(label.geometry().width(), 0, 100, 20)
        picture = QLabel(parent=self)
        pixmap = QPixmap('pics/pump_stopped.png')
        transform = QTransform()
        transform.rotate(90 * rotation.value)
        pixmap = pixmap.transformed(transform)
        picture.setPixmap(pixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Очистка воды HMI")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background: white; background-image: url(pics/back.png)")
        item = Item(self, "B1", RotateDir.ROT_UP)
        item.move(100, 100)
        self.show()


app = QApplication(sys.argv)
window = MainWindow()
app.exec()
