from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QComboBox, QVBoxLayout, QHBoxLayout

from misc import di
from misc.own_types import TankNumber
from widgets.brics import SLabel, SButton, SCombo
from widgets.seq_window import SeqWindow


class TankStroke(QWidget):
    def __init__(self, tankNumber: TankNumber):
        super(TankStroke, self).__init__()
        self.seqWindow = None
        self.tankNumber = tankNumber
        self.labelTextList = ["Бак чистой воды", "Бак отстойник 1", "Бак отстойник 2", "Бак отстойник 3"]
        self.setGeometry(0, 0, 300, 30)
        self.label = SLabel(self.labelTextList[tankNumber.value] + ", текущий шаг: ", transparent=True, color="gray")
        self.stepLabel = SLabel("Х", transparent=True)
        self.seqButton = SButton("Последовательность")
        self.box = QHBoxLayout()
        self.box.addWidget(self.label)
        self.box.addWidget(self.stepLabel)
        self.box.addWidget(self.seqButton)
        self.setLayout(self.box)
        for i in range(3):
            self.box.setStretch(i, 1)
        self.box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.seqButton.clicked.connect(self.clickOnButton)
        self.setMouseTracking(True)

    def clickOnButton(self):
        self.seqWindow = SeqWindow(self.labelTextList[self.tankNumber.value], self.tankNumber)
        self.seqWindow.show()


class ComStroke(QWidget):
    def __init__(self):
        super(ComStroke, self).__init__()
        self.statusList = ["X", "V"]
        self.statusColorList = ["red", "green"]
        self.setGeometry(0, 0, 300, 30)
        self.connectLabel = SLabel("Выбор COM-порта:", color="gray", transparent=True)
        self.connectCombo = SCombo()
        self.connectCombo.addItems(["COM1", "COM2"])
        self.connectButton = SButton("Подключиться к МК")
        self.statusLabel = SLabel(self.statusList[0], color="white", background="red")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box = QHBoxLayout()
        self.box.addWidget(self.connectLabel)
        self.box.addWidget(self.connectCombo)
        self.box.addWidget(self.connectButton)
        self.box.addWidget(self.statusLabel)
        for i in range(4):
            self.box.setStretch(i, 1)
        self.setLayout(self.box)
        self.box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.setMouseTracking(True)


class ControlPanel(QWidget):
    def __init__(self):
        super(ControlPanel, self).__init__()

        self.setParent(di.Container.mainWindow())
        self.setGeometry(225, 600, 600, 200)

        self.chbSeqPanel = TankStroke(TankNumber.CHB)
        self.ob1SeqPanel = TankStroke(TankNumber.OB1)
        self.ob2SeqPanel = TankStroke(TankNumber.OB2)
        self.ob3SeqPanel = TankStroke(TankNumber.OB3)
        self.comStroke = ComStroke()

        self.box = QVBoxLayout()
        self.box.addWidget(self.chbSeqPanel)
        self.box.addWidget(self.ob1SeqPanel)
        self.box.addWidget(self.ob2SeqPanel)
        self.box.addWidget(self.ob3SeqPanel)
        self.box.addWidget(self.comStroke)
        self.setStyleSheet("background: lightgray")
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        for i in range(6):
            self.box.setStretch(i, 1)
        self.setLayout(self.box)
        self.setMouseTracking(True)
