from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication

from panels.control_panel import ControlPanel
from panels.item import Item
from misc import di
from panels.sensor_mon import SensorMon
from misc.own_types import ObjectType, RotateDir, TankNumber


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
        super().__init__()
        self.setWindowTitle("Очистка воды HMI")
        self.setFixedSize(1200, 820)
        self.setStyleSheet("background: white; background-image: url(pics/back.png)")
        self.mousePos = None
        self.controlPanel = None
        self.setMouseTracking(True)
        self.setWindowIcon(QIcon('pics/icons/main.png'))

    def init(self, enableMousePosVis=False):
        self.M1 = Item("M1", ObjectType.PUMP, QPoint(265, 185), RotateDir.LEFT, TankNumber.OB1)
        self.M2 = Item("M2", ObjectType.PUMP, QPoint(495, 187), RotateDir.LEFT, TankNumber.OB2)
        self.M3 = Item("M3", ObjectType.PUMP, QPoint(723, 187), RotateDir.LEFT, TankNumber.OB3)
        self.M7 = Item("M6", ObjectType.PUMP, QPoint(921, 743), RotateDir.LEFT, TankNumber.CHB)
        self.M7 = Item("M7", ObjectType.PUMP, QPoint(804, 542), RotateDir.RIGHT, TankNumber.CHB)
        self.C1 = Item("C1", ObjectType.VALVE, QPoint(185, 90), RotateDir.DOWN, TankNumber.OB1)
        self.C2 = Item("C2", ObjectType.VALVE, QPoint(410, 90), RotateDir.DOWN, TankNumber.OB2)
        self.C3 = Item("C3", ObjectType.VALVE, QPoint(639, 90), RotateDir.DOWN, TankNumber.OB3)
        self.D1 = Item("D1", ObjectType.VALVE, QPoint(106, 390), RotateDir.DOWN, TankNumber.OB1)
        self.D2 = Item("D2", ObjectType.VALVE, QPoint(336, 390), RotateDir.DOWN, TankNumber.OB2)
        self.D3 = Item("D3", ObjectType.VALVE, QPoint(563, 390), RotateDir.DOWN, TankNumber.OB3)
        self.D4 = Item("D4", ObjectType.VALVE, QPoint(680, 580), RotateDir.LEFT, TankNumber.CHB)
        self.O1 = Item("O1", ObjectType.VALVE, QPoint(276, 465), RotateDir.DOWN, TankNumber.OB1)
        self.O2 = Item("O2", ObjectType.VALVE, QPoint(502, 465), RotateDir.DOWN, TankNumber.OB2)
        self.O3 = Item("O3", ObjectType.VALVE, QPoint(730, 465), RotateDir.DOWN, TankNumber.OB3)
        self.B1 = SensorMon("B1", QPoint(228, 240))
        self.H1 = SensorMon("H1", QPoint(228, 285))
        self.B2 = SensorMon("B2", QPoint(455, 239))
        self.H2 = SensorMon("H2", QPoint(455, 284))
        self.B3 = SensorMon("B3", QPoint(682, 239))
        self.H3 = SensorMon("H3", QPoint(682, 283))
        self.S4 = SensorMon("S4", QPoint(930, 585))
        self.S5 = SensorMon("S5", QPoint(930, 620))
        self.S6 = SensorMon("S6", QPoint(930, 655))
        self.mousePos = di.Container.mousePos(enableMousePosVis)
        self.controlPanel = ControlPanel()
        self.show()

    def mouseMoveEvent(self, event):
        self.mousePos.updatePos(event.pos().x(), event.pos().y())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape.value:
            for window in QApplication.topLevelWidgets():
                if window == self:
                    continue
                window.close()

    def closeEvent(self, event):
        di.Container.comm().disconnect()
        QApplication.closeAllWindows()
