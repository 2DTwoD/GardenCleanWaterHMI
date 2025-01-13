from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIntValidator
from PyQt6.QtWidgets import QLabel, QPushButton, QComboBox, QLineEdit

from misc.own_types import Align


class SFont(QFont):
    def __init__(self, size, bold=False):
        super(SFont, self).__init__('Sans Serif', size)
        self.setBold(bold)


class SLabel(QLabel):
    def __init__(self, text, parent=None, size=10, color="black", background="white", transparent=False, wordWrap=True,
                 maxWidth=None, align: Align = Align.VCENTER):
        super(SLabel, self).__init__(parent=parent)
        self.setText(text)
        if transparent:
            self.setStyleSheet(f"color: {color};background: transparent")
        else:
            self.setStyleSheet(f"color: {color};background:{background}")
        self.setWordWrap(wordWrap)
        self.setFont(SFont(size))
        self.setMouseTracking(True)
        if maxWidth is not None:
            self.setMaximumWidth(maxWidth)
        self.setAlignment(align.value)


class SButton(QPushButton):
    def __init__(self, text, parent=None, color="black", background="lightgray", fontSize=10):
        super(QPushButton, self).__init__(text, parent=parent)
        self.setFont(SFont(size=fontSize))
        self.setStyleSheet(f"color: {color};background:{background}")
        self.setMouseTracking(True)
        self.setMaximumSize(9999, 9999)


class SCombo(QComboBox):
    def __init__(self, parent=None, color="black", background="lightgray", fontSize=10):
        super(QComboBox, self).__init__(parent=parent)
        self.setFont(SFont(size=fontSize))
        self.setStyleSheet(f"color: {color};background:{background}")
        self.setMouseTracking(True)
        self.setMaximumSize(9999, 9999)


class SField(QLineEdit):
    def __init__(self, parent=None, color="black", background="white", fontSize=10, length=None, numeric=False,
                 minNum=0, maxNum=100):
        super(QLineEdit, self).__init__(parent=parent)
        self.setFont(SFont(size=fontSize))
        self.setStyleSheet(f"color: {color};background:{background}")
        if length is not None:
            self.setMaxLength(length)
        if numeric:
            self.setValidator(QIntValidator(minNum, maxNum, self))
        self.setMouseTracking(True)
        self.setMaximumSize(9999, 9999)
