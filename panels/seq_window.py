from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QGridLayout

from misc import di
from misc.own_types import TankNumber, Align, getGeometryStep
from misc.updater import Updater
from widgets.brics import SLabel, SButton, SField
from widgets.dialog import Confirm

statusList = ["Ожидание", "Активен", "Заблокир.", "Завершен", "Не определён"]
statusColorList = ["lightgray", "lightblue", "yellow", "lightgreen", "red"]
stepBackgroundList = ["lightgray", "lightblue"]
autoButtonColors = ["lightgray", "#00FF00", "yellow"]

class SeqStroke(list):
    def __init__(self, stepNumber, desc, actionDesc, startDesc="Всегда", lockDesc="Ручной режим",
                 endDesc="Не указано", timerEN=False, timerVarName="undefined"):
        super().__init__()

        self.stepNumber = stepNumber

        self.stepLabel = SLabel(f"Шаг {stepNumber}")
        self.statusLabel = SLabel(statusList[0], background=statusColorList[0])
        self.descLabel = SLabel(desc)
        self.actionLabel = SLabel(actionDesc)
        self.startLabel = SLabel(startDesc)
        self.lockLabel = SLabel(lockDesc)
        self.endLabel = SLabel(endDesc)

        self.append(self.stepLabel)
        self.append(self.statusLabel)
        self.append(self.descLabel)
        self.append(self.actionLabel)
        self.append(self.startLabel)
        self.append(self.lockLabel)
        self.append(self.endLabel)

        if timerEN:
            self.comm = di.Container.comm()
            self.timerVarName = timerVarName

            self.timeRemainLabel = SLabel("0")
            self.periodLabel = SLabel("0")
            self.editPeriodLine = SField(numeric=True, minNum=1, maxNum=999999, length=6, width=50)
            self.applyButton = SButton("Применить")

            self.append(self.periodLabel)
            self.append(self.timeRemainLabel)
            self.append(self.editPeriodLine)
            self.append(self.applyButton)

            self.applyButton.clicked.connect(self.applyButonClicked)

    def setStatus(self, status):
        self.statusLabel.setText(statusList[status])
        self.statusLabel.setBackground(statusColorList[status])

    def setStepBackground(self, currentStep):
        self.stepLabel.setBackground(stepBackgroundList[currentStep == self.stepNumber])

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
        value = self.editPeriodLine.text()
        if Confirm(f"Применить значение {value}?").cancel():
            return
        try:
            value = int(value)
        except:
            print("Неправильный ввод")
            return
        self.comm.send(f"[set.{self.timerVarName}.{value * 1000}]")


class SeqWindow(QWidget, Updater):
    def __init__(self, windowTitle, tankNumber: TankNumber):
        super().__init__()
        self.tankValues = di.Container.tankValues()
        self.comm = di.Container.comm()
        mousePos = di.Container.mousePos()
        self.tankNumber = tankNumber
        self.windowTitle = windowTitle
        self.rowNum = 0

        self.grid = QGridLayout()
        self.grid.setSpacing(3)

        self.addRow(self.getHeader())
        if tankNumber == TankNumber.CHB:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет", startDesc="Уровень ниже S5",
                                         endDesc="В очереди есть бочка отстойника")
            self.step2Stroke = SeqStroke(2, "Заполнение M7", "Открыть D4",
                                         endDesc="По таймеру", timerEN=True, timerVarName="chbs2per")
            self.step3Stroke = SeqStroke(3, "Наполнение чистой бочки", "Старт M7",
                                         lockDesc="Уровень выше S4 или ручной режим", endDesc="Бочка отстойника опорожнена или очередь пуста")
            self.addRow(self.step1Stroke)
            self.addRow(self.step2Stroke)
            self.addRow(self.step3Stroke)
            self.setFixedSize(85 * getGeometryStep(), 23 * getGeometryStep())
        else:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет",
                                         endDesc=f"Уровень ниже H{tankNumber.value}")
            self.step2Stroke = SeqStroke(2, "Слив остатка", f"Открыть D{tankNumber.value}",
                                         endDesc="По таймеру", timerEN=True, timerVarName=f"ob{tankNumber.value}s2per")
            self.step3Stroke = SeqStroke(3, "Промывка",
                                         f"Открыть C{tankNumber.value}, D{tankNumber.value}",
                                         endDesc="По таймеру", timerEN=True, timerVarName=f"ob{tankNumber.value}s3per")
            self.step4Stroke = SeqStroke(4, "Наполнение",
                                         f"Открыть C{tankNumber.value}, старт M{tankNumber.value} по таймеру",
                                         endDesc=f"Уровень выше В{tankNumber.value}", timerEN=True,
                                         timerVarName=f"ob{tankNumber.value}s4per")
            self.step5Stroke = SeqStroke(5, "Выдержка", "Нет",
                                         endDesc="По таймеру", timerEN=True, timerVarName=f"ob{tankNumber.value}s5per")
            self.step6Stroke = SeqStroke(6, "Опорожнение", f"Открыть O{tankNumber.value}",
                                         startDesc="Разрешение от чистой бочки",
                                         lockDesc="Уровень выше S4 или ручной режим",
                                         endDesc=f"Уровень ниже H{tankNumber.value}")
            self.addRow(self.step1Stroke)
            self.addRow(self.step2Stroke)
            self.addRow(self.step3Stroke)
            self.addRow(self.step4Stroke)
            self.addRow(self.step5Stroke)
            self.addRow(self.step6Stroke)
            self.setFixedSize(85 * getGeometryStep(), 33 * getGeometryStep())

        self.autoButton = SButton("Автомат", color="black", background=autoButtonColors[0])
        self.manButton = SButton("Ручной", color="black", background=autoButtonColors[0])
        self.nextButton = SButton("Пропустить шаг", color="black", background="orange")
        self.resetButton = SButton("Сброс последовательности", color="white", background="red")

        self.grid.addWidget(self.autoButton, self.rowNum, 0, 1, 2)
        self.grid.addWidget(self.manButton, self.rowNum, 2, 1, 1)
        self.grid.addWidget(self.nextButton, self.rowNum, 3, 1, 2)
        self.grid.addWidget(self.resetButton, self.rowNum, 5, 1, 2)

        self.autoButton.clicked.connect(lambda: self.autoManButton(1))
        self.manButton.clicked.connect(lambda: self.autoManButton(0))
        self.nextButton.clicked.connect(self.nextStep)
        self.resetButton.clicked.connect(self.resetSeq)

        self.setWindowTitle(windowTitle)
        self.setStyleSheet("background: gray")
        self.setLayout(self.grid)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.move(mousePos.getGlobalPos().x() - int(self.geometry().width() / 2),
                  mousePos.getGlobalPos().y() - self.geometry().height() - 50)
        self.startUpdate()
        self.setWindowIcon(QIcon('pics/icons/tank.png'))

    def resetSeq(self):
        if Confirm("Сбросить последовательность?").cancel():
            return
        if self.tankNumber == TankNumber.CHB:
            self.comm.send("[set.chbagain]")
        else:
            self.comm.send(f"[set.ob{self.tankNumber.value}again]")

    def nextStep(self):
        if Confirm("Пропустить шаг?").cancel():
            return
        if self.tankNumber == TankNumber.CHB:
            self.comm.send("[set.chbnext.1]")
        else:
            self.comm.send(f"[set.ob{self.tankNumber.value}next.1]")

    def autoManButton(self, value):
        if self.tankValues.get(self.tankNumber, "auto") == value:
            return
        message = f"Перевести '{self.windowTitle}' в автоматический режим?" if value > 0 else \
            f"Перевести '{self.windowTitle}' в ручной режим?"
        if Confirm(message).cancel():
            return
        if self.tankNumber == TankNumber.CHB:
            self.comm.send(f"[set.chbauto.{value}]")
        else:
            self.comm.send(f"[set.ob{self.tankNumber.value}auto.{value}]")

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

        auto = self.tankValues.get(self.tankNumber, "auto")
        self.autoButton.setBackground(autoButtonColors[int(auto)])
        self.manButton.setBackground(autoButtonColors[2 - int(auto) * 2])


    @staticmethod
    def updateStroke(stroke: SeqStroke, step, status, timeRemain=None, period=None):
        stroke.setStepBackground(step)
        stroke.setStatus(status)
        if (timeRemain is not None) and (period is not None):
            stroke.setTimeRemain(timeRemain)
            stroke.setPeriod(period)

    def closeEvent(self, event):
        self.stopUpdate()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape.value:
            self.close()

    def addRow(self, widgetList):
        for index, widget in enumerate(widgetList):
            self.grid.addWidget(widget, self.rowNum, index)
        self.rowNum += 1

    def getHeader(self):
        return [SLabel("Номер шага", background="black", color="white", align=Align.CENTER),
                SLabel("Статус", background="black", color="white", align=Align.CENTER),
                SLabel("Описание", background="black", color="white", align=Align.CENTER),
                SLabel("Действие", background="black", color="white", align=Align.CENTER),
                SLabel("Условие старта", background="black", color="white", align=Align.CENTER),
                SLabel("Блокировка", background="black", color="white", align=Align.CENTER),
                SLabel("Условие завершения", background="black", color="white", align=Align.CENTER),
                SLabel("Всё время", background="black", color="white", align=Align.CENTER),
                SLabel("Осталось", background="black", color="white", align=Align.CENTER),
                SLabel("Ввод, сек.", background="black", color="white", align=Align.CENTER),
                SLabel("Применить", background="black", color="white", align=Align.CENTER)]
