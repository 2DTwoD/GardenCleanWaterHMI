from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class SLabel(QLabel):
    def __init__(self, text, size=11, color="black", background="white", transparent=False):
        super(SLabel, self).__init__()
        self.setText(text)
        font = QFont('Times', size)
        font.setBold(True)
        if transparent:
            self.setStyleSheet(f"color: {color};background: transparent")
        else:
            self.setStyleSheet(f"color: {color};background:{background}")
        self.setFont(font)
