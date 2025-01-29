from PyQt6.QtWidgets import QWidget, QGridLayout

from misc import di
from misc.own_types import TankNumber, Align, getGeometryStep
from misc.updater import Updater
from widgets.brics import SLabel, SButton, SCombo
from panels.seq_window import SeqWindow
from widgets.dialog import Confirm

tankLabelList = ["Бак чистой воды", "Бак отстойник 1", "Бак отстойник 2", "Бак отстойник 3"]
autoButtonColors = ["lightgray", "#00FF00", "yellow"]
comStatusColorList = ["red", "green"]
comButtonColorList = ["gray", "lightgray"]
obStepDescList = ["Подготовка", "Слив", "Промывка", "Наполнение", "Выдержка", "Опорожн."]
chbStepDescList = ["Подготовка", "Заполн. М7", "Наполнение"]

class TankStroke(list):
    def __init__(self, tankNumber: TankNumber):
        super().__init__()

        self.comm = di.Container.comm()
        self.tankNumber = tankNumber
        self.seqWindow = None

        self.label = SLabel(tankLabelList[tankNumber.value], transparent=True, color="gray",
                            align=Align.VCENTER, bold=True)
        self.stepLabel = SLabel("Шаг Х", transparent=True, align=Align.VCENTER)
        self.autoButton = SButton("Автомат")
        self.manButton = SButton("Ручной")
        self.seqButton = SButton("Шаги")

        self.append(self.label)
        self.append(self.stepLabel)
        self.append(self.autoButton)
        self.append(self.manButton)
        self.append(self.seqButton)

        self.seqButton.clicked.connect(self.clickOnButton)
        self.autoButton.clicked.connect(lambda: self.autoManButton(1))
        self.manButton.clicked.connect(lambda: self.autoManButton(0))

    def clickOnButton(self):
        if self.seqWindow is not None:
            self.seqWindow.close()
        self.seqWindow = SeqWindow(tankLabelList[self.tankNumber.value], self.tankNumber)
        self.seqWindow.show()

    def setStepVis(self, curStep):
        if self.tankNumber == TankNumber.CHB:
            self.stepLabel.setText(f"Шаг {curStep}({chbStepDescList[curStep - 1]})")
        else:
            self.stepLabel.setText(f"Шаг {curStep}({obStepDescList[curStep - 1]})")

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


class MiscStroke(list):
    def __init__(self):
        super().__init__()

        self.comm = di.Container.comm()
        self.tankValues = di.Container.tankValues()

        self.queueLabel = SLabel("Очередь опорожнения:", transparent=True, align=Align.VCENTER,
                                 color="gray", bold=True)
        self.tankQueue = SLabel("Очередь пуста", size=12, transparent=True, align=Align.VCENTER)
        self.autoAllButton = SButton("Всё в автомат", background="green", color="white")
        self.manAllButton = SButton("Всё в ручной", background="orange")
        self.stopAllButton = SButton("Остановить всё", background="red", color="white")

        self.append(self.queueLabel)
        self.append(self.tankQueue)
        self.append(self.autoAllButton)
        self.append(self.manAllButton)
        self.append(self.stopAllButton)

        self.autoAllButton.clicked.connect(lambda: self.autoManAll(1))
        self.manAllButton.clicked.connect(lambda: self.autoManAll(0))
        self.stopAllButton.clicked.connect(self.stopAll)

    def autoManAll(self, value):
        message = "Перевести всё в автомат?" if value > 0 else "Перевести всё в ручной режим?"
        if Confirm(message).cancel():
            return
        self.comm.send(f"[set.allauto.{value}]")

    def stopAll(self):
        if Confirm("Остановить всё, что в ручном режиме?").cancel():
            return
        self.comm.send(f"[set.all.0]")

    def updateQueue(self, text):
        self.tankQueue.setText(self.getQueueLabelText(text))

    @staticmethod
    def getQueueLabelText(rawQueue: str):
        result = ""
        for c in rawQueue:
            if c != "0":
                result += c + "-->"
        if not result:
            return "Очередь пуста"
        return result[:-3]

class ComStroke(list):
    def __init__(self):
        super().__init__()

        self.comm = di.Container.comm()
        ports = self.comm.getAvailablePorts()
        ports.sort()

        self.connectLabel = SLabel("Выбор COM-порта:", color="gray", transparent=True, bold=True)
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
        if self.comm.connected() and Confirm("Отключиться от МК?").cancel():
            return
        self.comm.disconnect()

    def setStatus(self, ok: bool, label: str):
        self.statusLabel.setBackground(comStatusColorList[ok])
        self.statusLabel.setText(label)
        self.connectButton.setBackground(comButtonColorList[self.comm.disconnected()])
        self.disconnectButton.setBackground(comButtonColorList[self.comm.connected()])

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
        self.miscStroke = MiscStroke()
        self.comStroke = ComStroke()

        self.addRow(self.ob1SeqPanel)
        self.addRow(self.ob2SeqPanel)
        self.addRow(self.ob3SeqPanel)
        self.addRow(self.chbSeqPanel)
        self.addRow(self.miscStroke)
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
        self.miscStroke.updateQueue(self.tankValues.get(TankNumber.CHB, "queue"))
        self.comStroke.setStatus(self.comm.connected(), self.comm.getStatus())
        self.comStroke.setSelectable(self.comm.disconnected())
        self.comStroke.updateAvailablePorts()


    @staticmethod
    def drawStepAuto(tankStroke: TankStroke, step, auto):
        tankStroke.setStepVis(step)
        tankStroke.setAutoVis(auto)

