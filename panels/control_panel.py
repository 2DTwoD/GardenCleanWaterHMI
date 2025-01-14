from PyQt6.QtWidgets import QWidget, QGridLayout

from misc import di
from misc.own_types import TankNumber, Align
from widgets.brics import SLabel, SButton, SCombo
from panels.seq_window import SeqWindow


class TankLabelList(list):
    def __init__(self):
        super(list, self).__init__()
        self.extend(["Бак чистой воды", "Бак отстойник 1", "Бак отстойник 2", "Бак отстойник 3"])


class TankStroke(list):
    def __init__(self, tankNumber: TankNumber):
        super(list, self).__init__()
        self.seqWindow = None
        self.tankNumber = tankNumber
        self.tankLabelList = di.TankLabelList()

        self.label = SLabel(self.tankLabelList[tankNumber.value], transparent=True, color="gray", align=Align.VCENTER)
        self.stepLabel = SLabel("Шаг Х", transparent=True, align=Align.VCENTER)
        self.seqButton = SButton("Последовательность")
        self.autoButton = SButton("Автомат")
        self.manButton = SButton("Ручной")

        self.append(self.label)
        self.append(self.stepLabel)
        self.append(self.seqButton)
        self.append(self.autoButton)
        self.append(self.manButton)

        self.seqButton.clicked.connect(self.clickOnButton)

    def clickOnButton(self):
        self.seqWindow = SeqWindow(self.tankLabelList[self.tankNumber.value], self.tankNumber)
        self.seqWindow.show()


class ComStroke(list):
    def __init__(self):
        super(list, self).__init__()
        self.statusList = ["X", "V"]
        self.statusColorList = ["red", "green"]
        self.connectLabel = SLabel("Выбор COM-порта:", color="gray", transparent=True)
        self.connectCombo = SCombo()
        self.connectCombo.addItems(["COM1", "COM2"])
        self.connectButton = SButton("Подключиться к МК")
        self.disconnectButton = SButton("Отключиться от МК")
        self.statusLabel = SLabel(self.statusList[0], color="white", background="red", align=Align.CENTER)

        self.append(self.connectLabel)
        self.append(self.connectCombo)
        self.append(self.connectButton)
        self.append(self.disconnectButton)
        self.append(self.statusLabel)


class ControlPanel(QWidget):
    def __init__(self):
        super(ControlPanel, self).__init__()

        self.grid = QGridLayout()
        self.grid.setSpacing(3)
        self.rowNum = 0

        self.setParent(di.Container.mainWindow())
        self.setGeometry(225, 600, 600, 200)
        self.chbSeqPanel = TankStroke(TankNumber.CHB)
        self.ob1SeqPanel = TankStroke(TankNumber.OB1)
        self.ob2SeqPanel = TankStroke(TankNumber.OB2)
        self.ob3SeqPanel = TankStroke(TankNumber.OB3)
        self.comStroke = ComStroke()
        self.tankQueue = SLabel("Очередь опорожнения: X-->X-->X", size=12, transparent=True, align=Align.CENTER)

        self.addRow(self.chbSeqPanel)
        self.addRow(self.ob1SeqPanel)
        self.addRow(self.ob2SeqPanel)
        self.addRow(self.ob3SeqPanel)
        self.grid.addWidget(self.tankQueue, self.rowNum, 0, 1, 5)
        self.rowNum += 1
        self.addRow(self.comStroke)

        self.setStyleSheet("background: lightgray")
        self.setLayout(self.grid)
        self.setMouseTracking(True)

    def addRow(self, widgetList):
        for index, widget in enumerate(widgetList):
            self.grid.addWidget(widget, self.rowNum, index)
        self.rowNum += 1
