import sys

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication

from misc import di

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("fonts/sserifer.fon")
    window = di.Container.mainWindow()
    window.init(enableMousePosVis=False)
    app.exec()