import sys

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication

from misc import di

version = "v1.1.0"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("fonts/sserifer.fon")
    window = di.Container.mainWindow(version=version, windowWidth=1200, windowHeight=800)
    window.init(enableMousePosVis=False)
    app.exec()