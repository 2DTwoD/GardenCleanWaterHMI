import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from misc import di
from misc.own_types import TankNumber, Align
from misc.updater import Updater
from widgets.brics import SLabel, SButton, SField


class StatusList(list):
    def __init__(self):
        super().__init__()
        self.extend(["Ожидание", "Активен", "Заблокирован", "Завершен", "Не определён"])


class StatusColors(list):
    def __init__(self):
        super().__init__()
        self.extend(["lightgray", "lightblue", "yellow", "lightgreen", "red"])


class SeqStroke(list):
    def __init__(self, stepNumber, desc, actionDesc, startDesc="Всегда", lockDesc="Нет",
                 endDesc="Не указано", timerEN=False, timerVarName="undefined"):
        super().__init__()
        self.stepNumber = stepNumber
        self.stepLabel = SLabel(f"Шаг {stepNumber}")
        self.descLabel = SLabel(desc)
        self.statusLabel = SLabel(di.Container.statusList()[0])
        self.actionLabel = SLabel(actionDesc)
        self.startLabel = SLabel(startDesc)
        self.lockLabel = SLabel(lockDesc)
        self.endLabel = SLabel(endDesc)
        self.append(self.stepLabel)
        self.append(self.descLabel)
        self.append(self.statusLabel)
        self.append(self.actionLabel)
        self.append(self.startLabel)
        self.append(self.lockLabel)
        self.append(self.endLabel)
        if timerEN:
            self.timeRemainLabel = SLabel("0")
            self.periodLabel = SLabel("0")
            self.editPeriodLine = SField(numeric=True, minNum=1, maxNum=999999, length=6, width=50)
            self.applyButton = SButton("Применить")
            self.timerVarName = timerVarName
            self.comm = di.Container.comm()
            self.append(self.periodLabel)
            self.append(self.timeRemainLabel)
            self.append(self.editPeriodLine)
            self.append(self.applyButton)
            self.applyButton.clicked.connect(self.applyButonClicked)

    def setStatus(self, status):
        self.statusLabel.setText(di.Container.statusList()[status])
        self.statusLabel.setBackground(di.Container.statusColors()[status])

    def setStepBackground(self, currentStep):
        background = "lightblue" if currentStep == self.stepNumber else "lightgray"
        self.stepLabel.setBackground(background)

    def setTimeRemain(self, timeRemainMillis):
        self.timeRemainLabel.setText(self.getTimeStroke(timeRemainMillis))

    def setPeriod(self, periodMillis):
        self.periodLabel.setText(self.getTimeStroke(periodMillis))

    def getTimeStroke(self, timeMillis):
        time = int(timeMillis / 1000)
        seconds = time % 60
        minutes = int(time / 60) % 60
        hours = int(time / 3600)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def applyButonClicked(self):
        try:
            value = int(self.editPeriodLine.text())
        except:
            return
        self.comm.send(f"[set.{self.timerVarName}.{value * 1000}]")


class SeqWindow(QWidget, Updater):
    def __init__(self, windowTitle, tankNumber: TankNumber):
        super().__init__()
        self.setWindowTitle(windowTitle)
        self.grid = QGridLayout()
        self.grid.setSpacing(3)
        self.rowNum = 0
        self.tankNumber = tankNumber
        self.tankValues = di.Container.tankValues()
        self.comm = di.Container.comm()
        self.setStyleSheet("background: gray")
        self.addRow(self.getHeader())
        if tankNumber == TankNumber.CHB:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет", startDesc="Уровень ниже S5",
                                         endDesc="В очереди есть бочка отстойника")
            self.step2Stroke = SeqStroke(2, "Заполнение M7", "Открыть D4",
                                         endDesc="По таймеру", timerEN=True, timerVarName="chbs2per")
            self.step3Stroke = SeqStroke(3, "Наполнение чистой бочки", "Старт M7",
                                         lockDesc="Уровень выше S4", endDesc="Бочка отстойника опорожнена")
            self.addRow(self.step1Stroke)
            self.addRow(self.step2Stroke)
            self.addRow(self.step3Stroke)
            self.setFixedSize(850, 230)
        else:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет",
                                         endDesc=f"Уровень ниже H{tankNumber.value}")
            self.step2Stroke = SeqStroke(2, "Слив остатка", f"Открыть D{tankNumber.value}",
                                         endDesc="По таймеру", timerEN=True, timerVarName=f"ob{tankNumber.value}s2per")
            self.step3Stroke = SeqStroke(3, "Промывка",
                                         f"Открыть C{tankNumber.value}, D{tankNumber.value}",
                                         endDesc="По таймеру", timerEN=True, timerVarName=f"ob{tankNumber.value}s3per")
            self.step4Stroke = SeqStroke(4, "Заполнение",
                                         f"Открыть C{tankNumber.value}, старт M{tankNumber.value} по таймеру",
                                         endDesc=f"Уровень выше В{tankNumber.value}", timerEN=True,
                                         timerVarName=f"ob{tankNumber.value}s4per")
            self.step5Stroke = SeqStroke(5, "Выдержка", "Нет",
                                         endDesc="По таймеру", timerEN=True, timerVarName=f"ob{tankNumber.value}s5per")
            self.step6Stroke = SeqStroke(6, "Опорожнение", f"Открыть O{tankNumber.value}",
                                         startDesc="Разрешение от чистой бочки", lockDesc="Уровень выше S4",
                                         endDesc=f"Уровень ниже H{tankNumber.value}")
            self.addRow(self.step1Stroke)
            self.addRow(self.step2Stroke)
            self.addRow(self.step3Stroke)
            self.addRow(self.step4Stroke)
            self.addRow(self.step5Stroke)
            self.addRow(self.step6Stroke)
            self.setFixedSize(850, 330)

        self.resetButton = SButton("Сброс последовательности", color="white", background="red")
        self.nextButton = SButton("Пропустить шаг", color="black", background="yellow")
        self.resetButton.clicked.connect(self.resetSeq)
        self.nextButton.clicked.connect(self.nextStep)
        self.grid.addWidget(self.resetButton, self.rowNum, 0, 1, 3)
        self.grid.addWidget(self.nextButton, self.rowNum, 3, 1, 2)

        self.setLayout(self.grid)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        mousePos = di.Container.mousePos()
        self.move(mousePos.getGlobalPos().x() - int(self.geometry().width() / 2),
                  mousePos.getGlobalPos().y() - self.geometry().height() - 50)
        self.startUpdate()

    def resetSeq(self):
        if self.tankNumber == TankNumber.CHB:
            self.comm.send("[set.chbstep.0]")
        else:
            self.comm.send(f"[set.ob{self.tankNumber.value}step.0]")

    def nextStep(self):
        if self.tankNumber == TankNumber.CHB:
            self.comm.send("[set.chbnext.1]")
        else:
            self.comm.send(f"[set.ob{self.tankNumber.value}next.1]")

    def updateAction(self):
        self.updateStroke(self.step1Stroke, self.tankValues.get(self.tankNumber, "step"),
                          self.tankValues.get(self.tankNumber, "s1St"))
        self.updateStroke(self.step2Stroke, self.tankValues.get(self.tankNumber, "step"),
                          self.tankValues.get(self.tankNumber, "s2St"),
                          self.tankValues.get(self.tankNumber, "s2TimeRem"),
                          self.tankValues.get(self.tankNumber, "s2Per"))
        if self.tankNumber == TankNumber.CHB:
            self.updateStroke(self.step3Stroke, self.tankValues.get(self.tankNumber, "step"),
                              self.tankValues.get(self.tankNumber, "s3St"))
        else:
            self.updateStroke(self.step3Stroke, self.tankValues.get(self.tankNumber, "step"),
                              self.tankValues.get(self.tankNumber, "s3St"),
                              self.tankValues.get(self.tankNumber, "s3TimeRem"),
                              self.tankValues.get(self.tankNumber, "s3Per"))
            self.updateStroke(self.step4Stroke, self.tankValues.get(self.tankNumber, "step"),
                              self.tankValues.get(self.tankNumber, "s4St"),
                              self.tankValues.get(self.tankNumber, "s4TimeRem"),
                              self.tankValues.get(self.tankNumber, "s4Per"))
            self.updateStroke(self.step5Stroke, self.tankValues.get(self.tankNumber, "step"),
                              self.tankValues.get(self.tankNumber, "s5St"),
                              self.tankValues.get(self.tankNumber, "s5TimeRem"),
                              self.tankValues.get(self.tankNumber, "s5Per"))
            self.updateStroke(self.step6Stroke, self.tankValues.get(self.tankNumber, "step"),
                              self.tankValues.get(self.tankNumber, "s6St"))
        self.resetButton.setEnabled(self.tankValues.get(self.tankNumber, "auto"))
        self.nextButton.setEnabled(self.tankValues.get(self.tankNumber, "auto"))

    @staticmethod
    def updateStroke(stroke: SeqStroke, step, status, timeRemain=None, period=None):
        stroke.setStepBackground(step)
        stroke.setStatus(status)
        if (timeRemain is not None) and (period is not None):
            stroke.setTimeRemain(timeRemain)
            stroke.setPeriod(period)

    def closeEvent(self, event):
        self.stopUpdate()

    def addRow(self, widgetList):
        for index, widget in enumerate(widgetList):
            self.grid.addWidget(widget, self.rowNum, index)
        self.rowNum += 1

    def getHeader(self):
        return [SLabel("Номер шага", background="black", color="white", align=Align.CENTER),
                SLabel("Описание", background="black", color="white", align=Align.CENTER),
                SLabel("Статус", background="black", color="white", align=Align.CENTER),
                SLabel("Действие", background="black", color="white", align=Align.CENTER),
                SLabel("Условие старта", background="black", color="white", align=Align.CENTER),
                SLabel("Блокировка", background="black", color="white", align=Align.CENTER),
                SLabel("Условие завершения", background="black", color="white", align=Align.CENTER),
                SLabel("Всё время", background="black", color="white", align=Align.CENTER),
                SLabel("Осталось", background="black", color="white", align=Align.CENTER),
                SLabel("Ввод, сек.", background="black", color="white", align=Align.CENTER),
                SLabel("Применить", background="black", color="white", align=Align.CENTER)]
