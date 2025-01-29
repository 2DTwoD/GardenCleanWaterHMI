from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QGridLayout

from misc.own_types import getGeometryStep, Align
from widgets.brics import SButton, SLabel


class Confirm(QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("Подтвердите действие")

        yesBut = SButton("Да")
        cancelBut = SButton("Отмена")
        message = SLabel(text, align=Align.CENTER, transparent=True)

        yesBut.clicked.connect(self.accept)
        cancelBut.clicked.connect(self.reject)

        grid = QGridLayout()
        grid.addWidget(message, 0, 0, 1, 2)
        grid.addWidget(yesBut, 1, 0, 1, 1)
        grid.addWidget(cancelBut, 1, 1, 1, 1)
        self.setLayout(grid)
        self.setFixedSize(25 * getGeometryStep(), 10 * getGeometryStep())
        self.setWindowIcon(QIcon('pics/icons/confirm.png'))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.WindowCloseButtonHint)

    def yes(self):
        return self.exec()

    def cancel(self):
        return not self.exec()