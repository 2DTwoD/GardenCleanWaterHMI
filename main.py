import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

from item import Item
from mouse_pos import MousePos
from sensor_mon import SensorMon
from own_types import ObjectType, Point, RotateDir


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
