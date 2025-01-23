from PyQt6.QtWidgets import QWidget, QGridLayout, QApplication

from misc import di
from misc.own_types import TankNumber, Align, getGeometryStep
from misc.updater import Updater
from widgets.brics import SLabel, SButton, SCombo
from panels.seq_window import SeqWindow

tankLabelList = ["Бак чистой воды", "Бак отстойник 1", "Бак отстойник 2", "Бак отстойник 3"]
autoButtonColors = ["lightgray", "#00FF00", "yellow"]
comStatusColorList = ["red", "green"]

class TankStroke(list):
    def __init__(self, tankNumber: TankNumber):
        super().__init__()

        self.comm = di.Container.comm()
        self.tankNumber = tankNumber
        self.seqWindow = None

        self.label = SLabel(tankLabelList[tankNumber.value], transparent=True, color="gray", align=Align.VCENTER)
        self.stepLabel = SLabel("Шаг Х", transparent=True, align=Align.VCENTER)
        self.seqButton = SButton("Шаги")
        self.autoButton = SButton("Автомат")
        self.manButton = SButton("Ручной")

        self.append(self.label)
        self.append(self.stepLabel)
        self.append(self.seqButton)
        self.append(self.autoButton)
        self.append(self.manButton)

        self.seqButton.clicked.connect(self.clickOnButton)
        self.autoButton.clicked.connect(lambda: self.autoManButton(1))
        self.manButton.clicked.connect(lambda: self.autoManButton(0))

    def clickOnButton(self):
        if self.seqWindow is not None:
            self.seqWindow.close()
        self.seqWindow = SeqWindow(tankLabelList[self.tankNumber.value], self.tankNumber)
        self.seqWindow.show()

    def setStepVis(self, curStep):
        self.stepLabel.setText(f"Шаг {curStep}")

    def setAutoVis(self, auto):
        autoColor = autoButtonColors[0]
        manColor = autoButtonColors[0]
        if auto > 0:
            autoColor = autoButtonColors[1]
        else:
            manColor = autoButtonColors[2]
        self.autoButton.setBackground(autoColor)
        self.manButton.setBackground(manColor)

    def autoManButton(self, value):
        if self.tankNumber == TankNumber.CHB:
            self.comm.send(f"[set.chbauto.{value}]")
        else:
            self.comm.send(f"[set.ob{self.tankNumber.value}auto.{value}]")


class ComStroke(list):
    def __init__(self):
        super().__init__()

        self.comm = di.Container.comm()
        ports = self.comm.getAvailablePorts()
        ports.sort()

        self.connectLabel = SLabel("Выбор COM-порта:", color="gray", transparent=True)
        self.connectCombo = SCombo()
        self.connectCombo.addItems(ports)
        self.connectButton = SButton("Подключиться")
        self.disconnectButton = SButton("Отключиться")
        self.statusLabel = SLabel("X", color="white", background="red", align=Align.CENTER, bold=True)

        self.append(self.connectLabel)
        self.append(self.connectCombo)
        self.append(self.connectButton)
        self.append(self.disconnectButton)
        self.append(self.statusLabel)

        self.connectButton.clicked.connect(self.connect)
        self.disconnectButton.clicked.connect(self.disconnect)

    def connect(self):
        self.comm.connect(self.connectCombo.currentText())

    def disconnect(self):
        self.comm.disconnect()

    def setStatus(self, ok: bool, label: str):
        self.statusLabel.setBackground(comStatusColorList[ok])
        self.statusLabel.setText(label)

    def setSelectable(self, value):
        self.connectCombo.setEnabled(value)

    def updateAvailablePorts(self):
        if self.comm.connected():
            return
        ports = self.comm.getAvailablePorts()
        ports.sort()
        allItems = [self.connectCombo.itemText(i) for i in range(self.connectCombo.count())]
        if ports == allItems:
            return
        self.connectCombo.clear()
        self.connectCombo.addItems(ports)


class ControlPanel(QWidget, Updater):
    def __init__(self):
        super().__init__()

        self.tankValues = di.Container.tankValues()
        self.comm = di.Container.comm()
        self.rowNum = 0

        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        self.chbSeqPanel = TankStroke(TankNumber.CHB)
        self.ob1SeqPanel = TankStroke(TankNumber.OB1)
        self.ob2SeqPanel = TankStroke(TankNumber.OB2)
        self.ob3SeqPanel = TankStroke(TankNumber.OB3)
        self.comStroke = ComStroke()
        self.queueLabel = SLabel("Очередь опорожнения:", transparent=True, align=Align.VCENTER, color="gray")
        self.tankQueue = SLabel("X-->X-->X", size=12, transparent=True, align=Align.VCENTER)

        self.addRow(self.ob1SeqPanel)
        self.addRow(self.ob2SeqPanel)
        self.addRow(self.ob3SeqPanel)
        self.addRow(self.chbSeqPanel)
        self.grid.addWidget(self.queueLabel, self.rowNum, 0, 1, 1)
        self.grid.addWidget(self.tankQueue, self.rowNum, 1, 1, 1)
        self.rowNum += 1
        self.addRow(self.comStroke)

        self.setStyleSheet("background: lightgray")
        self.setLayout(self.grid)
        self.setParent(di.Container.mainWindow())
        self.setGeometry(int(17.5 * getGeometryStep()), 60 * getGeometryStep(),
                         65 * getGeometryStep(), 20 * getGeometryStep())
        self.setMouseTracking(True)
        self.startUpdate()

    def addRow(self, widgetList):
        for index, widget in enumerate(widgetList):
            self.grid.addWidget(widget, self.rowNum, index)
        self.rowNum += 1

    def updateAction(self):
        self.drawStepAuto(self.chbSeqPanel, self.tankValues.get(TankNumber.CHB, "step"),
                          self.tankValues.get(TankNumber.CHB, "auto"))
        self.drawStepAuto(self.ob1SeqPanel, self.tankValues.get(TankNumber.OB1, "step"),
                          self.tankValues.get(TankNumber.OB1, "auto"))
        self.drawStepAuto(self.ob2SeqPanel, self.tankValues.get(TankNumber.OB2, "step"),
                          self.tankValues.get(TankNumber.OB2, "auto"))
        self.drawStepAuto(self.ob3SeqPanel, self.tankValues.get(TankNumber.OB3, "step"),
                          self.tankValues.get(TankNumber.OB3, "auto"))
        self.tankQueue.setText(self.getQueueLabelText(self.tankValues.get(TankNumber.CHB, "queue")))
        self.comStroke.setStatus(self.comm.connected(), self.comm.getStatus())
        self.comStroke.setSelectable(self.comm.disconnected())
        self.comStroke.updateAvailablePorts()


    @staticmethod
    def drawStepAuto(tankStroke: TankStroke, step, auto):
        tankStroke.setStepVis(step)
        tankStroke.setAutoVis(auto)

    @staticmethod
    def getQueueLabelText(rawQueue: str):
        result = ""
        for c in rawQueue:
            if c != "0":
                result += c + "-->"
        if not result:
            return "Очередь пуста"
        return result[:-3]
