from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QMainWindow, QApplication

import di as DI
from item import Item
from sensor_mon import SensorMon
from own_types import ObjectType, RotateDir


class MainWindow(QMainWindow):
    M1: Item = None
    M2: Item = None
    M3: Item = None
    M7: Item = None
    C1: Item = None
    C2: Item = None
    C3: Item = None
    D1: Item = None
    D2: Item = None
    D3: Item = None
    D4: Item = None
    O1: Item = None
    O2: Item = None
    O3: Item = None
    B1: SensorMon = None
    H1: SensorMon = None
    B2: SensorMon = None
    H2: SensorMon = None
    B3: SensorMon = None
    H3: SensorMon = None
    S4: SensorMon = None
    S5: SensorMon = None
    S6: SensorMon = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Очистка воды HMI")
        self.setFixedSize(1200, 800)
        self.setStyleSheet("background: white; background-image: url(pics/back.png)")
        self.mousePos = None
        self.setMouseTracking(True)
        # self.but = QPushButton("херачь!", parent=self)
        # self.but.released.connect(lambda: self.the_button_was_clicked(self.sens))
        # self.but.move(800, 300)

    # def the_button_was_clicked(self, sens):
    #     sens.wid += 1
    #     sens.update()

    def di_init(self):
        self.M1 = Item("M1", ObjectType.PUMP, QPoint(265, 185), RotateDir.LEFT)
        #DI.Container.item(text="M1", type=ObjectType.PUMP, position=QPoint(265, 185), rotation=RotateDir.LEFT)
        self.M2 = Item("M2", ObjectType.PUMP, QPoint(495, 187), RotateDir.LEFT)
        self.M3 = Item("M3", ObjectType.PUMP, QPoint(723, 187), RotateDir.LEFT)
        self.M7 = Item("M6", ObjectType.PUMP, QPoint(921, 743), RotateDir.LEFT)
        self.M7 = Item("M7", ObjectType.PUMP, QPoint(804, 542), RotateDir.RIGHT)
        self.C1 = Item("C1", ObjectType.VALVE, QPoint(185, 90), RotateDir.DOWN)
        self.C2 = Item("C2", ObjectType.VALVE, QPoint(410, 90), RotateDir.DOWN)
        self.C3 = Item("C3", ObjectType.VALVE, QPoint(639, 90), RotateDir.DOWN)
        self.D1 = Item("D1", ObjectType.VALVE, QPoint(106, 390), RotateDir.DOWN)
        self.D2 = Item("D2", ObjectType.VALVE, QPoint(336, 390), RotateDir.DOWN)
        self.D3 = Item("D3", ObjectType.VALVE, QPoint(563, 390), RotateDir.DOWN)
        self.D4 = Item("D4", ObjectType.VALVE, QPoint(680, 580), RotateDir.LEFT)
        self.O1 = Item("O1", ObjectType.VALVE, QPoint(276, 465), RotateDir.DOWN)
        self.O2 = Item("O2", ObjectType.VALVE, QPoint(502, 465), RotateDir.DOWN)
        self.O3 = Item("O3", ObjectType.VALVE, QPoint(730, 465), RotateDir.DOWN)
        self.B1 = SensorMon("B1", QPoint(228, 240))
        self.H1 = SensorMon("H1", QPoint(228, 285))
        self.B2 = SensorMon("B2", QPoint(455, 239))
        self.H2 = SensorMon("H2", QPoint(455, 284))
        self.B3 = SensorMon("B3", QPoint(682, 239))
        self.H3 = SensorMon("H3", QPoint(682, 283))
        self.S4 = SensorMon("S4", QPoint(930, 585))
        self.S5 = SensorMon("S5", QPoint(930, 620))
        self.S6 = SensorMon("S6", QPoint(930, 655))
        self.mousePos = DI.Container.mousePos()
        self.show()

    def mouseMoveEvent(self, event):
        try:
            self.mousePos.updatePos(event.pos().x(), event.pos().y())
        except Exception as msg:
            print('Error with mouse move: ' + str(msg))

    def closeEvent(self, event):
        QApplication.closeAllWindows()

