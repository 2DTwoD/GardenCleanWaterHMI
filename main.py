import sys
from PyQt6.QtWidgets import QApplication
from misc import di

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = di.Container.mainWindow()
    window.init()
    app.exec()
