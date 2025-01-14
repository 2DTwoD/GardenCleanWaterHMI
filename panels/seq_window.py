from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from misc import di
from misc.own_types import TankNumber, Align
from widgets.brics import SLabel, SButton, SField


class StatusList(list):
    def __init__(self):
        super(list, self).__init__()
        self.extend(["Ожидание", "Активен", "Заблокирован", "Завершен", "Неопределенный статус"])


class SeqStroke(list):
    def __init__(self, stepNumber, desc, actionDesc, startDesc="Всегда", lockDesc="Нет",
                 endDesc="Не указано", timerEN=False):
        super(list, self).__init__()
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
            self.editPeriodLine = SField(numeric=True, minNum=1, maxNum=99999, length=5)
            self.applyButton = SButton("Применить")
            self.append(self.timeRemainLabel)
            self.append(self.periodLabel)
            self.append(self.editPeriodLine)
            self.append(self.applyButton)

    def setStatus(self, status):
        self.statusLabel.setText(di.Container.statusList()[status])


class SeqWindow(QWidget):
    def __init__(self, windowTitle, tankNumber: TankNumber):
        super(SeqWindow, self).__init__()
        self.setWindowTitle(windowTitle)
        self.grid = QGridLayout()
        self.grid.setSpacing(3)
        self.rowNum = 0
        self.setStyleSheet("background: gray")
        self.addRow(self.getHeader())
        if tankNumber == TankNumber.CHB:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет", startDesc="Уровень выше S5",
                                         endDesc="В очереди есть бочка отстойника")
            self.step2Stroke = SeqStroke(2, "Заполнение M7", "Открыть D4", endDesc="По таймеру", timerEN=True)
            self.step3Stroke = SeqStroke(3, "Наполнение чистой бочки", "Старт M7", lockDesc="Уровень выше S4",
                                         endDesc="Бочка отстойника опорожнена")
            self.addRow(self.step1Stroke)
            self.addRow(self.step2Stroke)
            self.addRow(self.step3Stroke)
            self.setFixedSize(800, 230)
        else:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет", endDesc=f"Уровень ниже H{tankNumber.value}")
            self.step2Stroke = SeqStroke(2, "Слив остатка", f"Открыть D{tankNumber.value}",
                                         endDesc="По таймеру", timerEN=True)
            self.step3Stroke = SeqStroke(3, "Промывка", f"Открыть C{tankNumber.value}, D{tankNumber.value}",
                                         endDesc="По таймеру", timerEN=True)
            self.step4Stroke = SeqStroke(4, "Заполнение",
                                         f"Открыть C{tankNumber.value}, старт M{tankNumber.value} по таймеру",
                                         endDesc=f"Уровень выше В{tankNumber.value}", timerEN=True)
            self.step5Stroke = SeqStroke(5, "Выдержка", "Нет",
                                         endDesc="По таймеру", timerEN=True)
            self.step6Stroke = SeqStroke(6, "Слив", f"Открыть O{tankNumber.value}",
                                         startDesc="Разрешение от чистой бочки", lockDesc="Уровень выше S4",
                                         endDesc=f"Уровень ниже H{tankNumber.value}")
            self.addRow(self.step1Stroke)
            self.addRow(self.step2Stroke)
            self.addRow(self.step3Stroke)
            self.addRow(self.step4Stroke)
            self.addRow(self.step5Stroke)
            self.addRow(self.step6Stroke)
            self.setFixedSize(800, 330)

        self.resetButton = SButton("Сброс последовательности", color="white", background="red")
        self.grid.addWidget(self.resetButton, self.rowNum, 0, 1, 3)

        self.setLayout(self.grid)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        mousePos = di.Container.mousePos()
        self.move(mousePos.getGlobalPos().x() - int(self.geometry().width() / 2), mousePos.getGlobalPos().y() - self.geometry().height() - 50)

    def addRow(self, widgetList):
        for index, widget in enumerate(widgetList):
            self.grid.addWidget(widget, self.rowNum, index)
        self.rowNum += 1

    def getHeader(self):
        return [SLabel("Номер шага", background="lightgray", align=Align.CENTER), SLabel("Описание", background="lightgray", align=Align.CENTER),
                SLabel("Статус", background="lightgray", align=Align.CENTER), SLabel("Действие", background="lightgray", align=Align.CENTER),
                SLabel("Условие старта", background="lightgray", align=Align.CENTER), SLabel("Блокировка", background="lightgray", align=Align.CENTER),
                SLabel("Условие завершения", background="lightgray", align=Align.CENTER), SLabel("Осталось времени", background="lightgray", align=Align.CENTER),
                SLabel("Период", background="lightgray", align=Align.CENTER), SLabel("Ввести знач., сек.", background="lightgray", align=Align.CENTER),
                SLabel("Применить", background="lightgray", align=Align.CENTER)]
