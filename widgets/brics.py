from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QPushButton, QComboBox


class SFont(QFont):
    def __init__(self, size, bold=False):
        super(SFont, self).__init__('Sans Serif', size)
        self.setBold(bold)


class SLabel(QLabel):
    def __init__(self, text, parent=None, size=10, color="black", background="white", transparent=False, wordWrap=True,
                 maxWidth=None):
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


class SButton(QPushButton):
    def __init__(self, text, color="black", background="lightgray", fontSize=10):
        super(QPushButton, self).__init__(text)
        self.setFont(SFont(size=fontSize))
        self.setStyleSheet(f"color: {color};background:{background}")
        self.setMouseTracking(True)


class SCombo(QComboBox):
    def __init__(self, color="black", background="lightgray", fontSize=10):
        super(QComboBox, self).__init__()
        self.setFont(SFont(size=fontSize))
        self.setStyleSheet(f"color: {color};background:{background}")
        self.setMouseTracking(True)
