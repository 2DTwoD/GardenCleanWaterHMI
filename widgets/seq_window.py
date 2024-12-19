from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from misc.own_types import TankNumber


class SeqStroke(QWidget):
    def __init__(self, tankNumber: TankNumber, stepNumber, desc, statusList):
        super(SeqStroke, self).__init__()

class SeqWindow(QWidget):
    def __init__(self, windowTitle, tankNumber: TankNumber):
        super(SeqWindow, self).__init__()
        self.setWindowTitle(windowTitle)
        self.box = QVBoxLayout()
        self.setLayout(self.box)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(500, 500)