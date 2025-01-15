from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import QLabel, QPushButton, QComboBox, QLineEdit

from misc.own_types import Align


class SFont(QFont):
    def __init__(self, size, bold=False):
        super().__init__('Sans Serif', size)
        self.setBold(bold)


class SLabel(QLabel):
    def __init__(self, text, parent=None, size=10, bold=False, color="black", background="white", transparent=False, wordWrap=True,
                 maxWidth=None, align: Align = Align.VCENTER):
        super().__init__(parent=parent)
        self.setText(text)
        self.color = color
        self.background = background
        if transparent:
            self.background = "transparent"
        self.updateColor()
        self.setWordWrap(wordWrap)
        self.setFont(SFont(size, bold=bold))
        self.setMouseTracking(True)
        if maxWidth is not None:
            self.setMaximumWidth(maxWidth)
        self.setAlignment(align.value)

    def setBackground(self, newColor):
        self.background = newColor
        self.updateColor()

    def updateColor(self):
        self.setStyleSheet(f"color: {self.color};background: {self.background}")

class SButton(QPushButton):
    def __init__(self, text, parent=None, color="black", background="lightgray", fontSize=10):
        super().__init__(text, parent=parent)
        self.setFont(SFont(size=fontSize))
        self.color = color
        self.background = background
        self.updateColor()
        self.setMouseTracking(True)
        self.setMaximumSize(9999, 9999)

    def setBackground(self, newColor):
        self.background = newColor
        self.updateColor()

    def updateColor(self):
        self.setStyleSheet(f"color: {self.color};background: {self.background}")

class SCombo(QComboBox):
    def __init__(self, parent=None, color="black", background="lightgray", fontSize=10):
        super().__init__(parent=parent)
        self.setFont(SFont(size=fontSize))
        self.setStyleSheet(f"color: {color};background:{background}")
        self.setMouseTracking(True)
        self.setMaximumSize(9999, 9999)


class SField(QLineEdit):
    def __init__(self, parent=None, color="black", background="white", fontSize=10, length=None, numeric=False,
                 minNum=0, maxNum=100, width=None):
        super().__init__(parent=parent)
        self.setFont(SFont(size=fontSize))
        self.setStyleSheet(f"color: {color};background:{background}")
        if length is not None:
            self.setMaxLength(length)
        if numeric:
            self.setValidator(QIntValidator(minNum, maxNum, self))
        self.setMouseTracking(True)
        self.setMaximumSize(9999, 9999)
        if width is not None:
            self.setFixedWidth(width)
