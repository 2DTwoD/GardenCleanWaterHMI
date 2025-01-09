from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from misc import di
from misc.own_types import TankNumber
from widgets.brics import SLabel


class StatusList(list):
    def __init__(self):
        super(StatusList, self).__init__()
        self.extend(["Ожидание", "Активен", "Заблокирован", "Завершен", "Неопределенный статус"])


class SeqStroke(QWidget):
    def __init__(self, stepNumber, desc, actionDesc, startDesc="Всегда", lockDesc="Нет",
                 endDesc="Не указано"):
        super(SeqStroke, self).__init__()
        self.stepLabel = SLabel(f"Шаг {stepNumber}", maxWidth=50)
        self.descLabel = SLabel(desc, maxWidth=100)
        self.statusLabel = SLabel(di.Container.statusList()[0], maxWidth=100)
        self.actionLabel = SLabel(actionDesc, maxWidth=100)
        self.startLabel = SLabel(startDesc, maxWidth=100)
        self.lockLabel = SLabel(lockDesc, maxWidth=100)
        self.endLabel = SLabel(endDesc, maxWidth=100)
        self.timeRemainLabel = SLabel("0", maxWidth=50)
        self.periodLabel = SLabel("0", maxWidth=50)

        self.editPeriodLine = QLineEdit()
        self.editPeriodLine.setMaximumWidth(50)
        self.editPeriodLine.setMaxLength(5)
        self.editPeriodLine.setValidator(QIntValidator(1, 99999, self))

        self.applyButton = QPushButton("Применить")

        self.box = QHBoxLayout()
        self.box.addWidget(self.stepLabel)
        self.box.addWidget(self.descLabel)
        self.box.addWidget(self.statusLabel)
        self.box.addWidget(self.actionLabel)
        self.box.addWidget(self.startLabel)
        self.box.addWidget(self.lockLabel)
        self.box.addWidget(self.endLabel)
        self.box.addWidget(self.timeRemainLabel)
        self.box.addWidget(self.periodLabel)
        self.box.addWidget(self.editPeriodLine)
        self.box.addWidget(self.applyButton)
        self.setLayout(self.box)


    def setStatus(self, status):
        self.statusLabel.setText(di.Container.statusList()[status])


class SeqWindow(QWidget):
    def __init__(self, windowTitle, tankNumber: TankNumber):
        super(SeqWindow, self).__init__()
        self.setWindowTitle(windowTitle)
        self.box = QVBoxLayout()
        if tankNumber == TankNumber.CHB:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет", startDesc="Уровень выше S5",
                                         endDesc="В очереди есть бочка отстойника")
            self.step2Stroke = SeqStroke(2, "Заполнение M7", "Открыть D4", endDesc="По таймеру")
            self.step3Stroke = SeqStroke(3, "Наполнение чистой бочки", "Старт M7", lockDesc="Уровень выше S4",
                                         endDesc="Бочка отстойника опорожнена")
            self.box.addWidget(self.step1Stroke)
            self.box.addWidget(self.step2Stroke)
            self.box.addWidget(self.step3Stroke)
        else:
            self.step1Stroke = SeqStroke(1, "Подготовка", "Нет", endDesc=f"Уровень ниже H{tankNumber.value}")
            self.step2Stroke = SeqStroke(2, "Слив остатка", f"Открыть D{tankNumber.value}",
                                         endDesc="По таймеру")
            self.step3Stroke = SeqStroke(3, "Промывка", f"Открыть C{tankNumber.value}, D{tankNumber.value}",
                                         endDesc="По таймеру")
            self.step4Stroke = SeqStroke(4, "Заполнение",
                                         f"Открыть C{tankNumber.value}, старт M{tankNumber.value} по таймеру",
                                         endDesc=f"Уровень выше В{tankNumber.value}")
            self.step5Stroke = SeqStroke(5, "Выдержка", "Нет",
                                         endDesc="По таймеру")
            self.step6Stroke = SeqStroke(6, "Слив", f"Открыть O{tankNumber.value}",
                                         startDesc="Разрешение от чистой бочки", lockDesc="Уровень выше S4",
                                         endDesc=f"Уровень ниже H{tankNumber.value}")
            self.box.addWidget(self.step1Stroke)
            self.box.addWidget(self.step2Stroke)
            self.box.addWidget(self.step3Stroke)
            self.box.addWidget(self.step4Stroke)
            self.box.addWidget(self.step5Stroke)
            self.box.addWidget(self.step6Stroke)
        self.setLayout(self.box)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(1000, 400)
