import sys
from PyQt6.QtWidgets import QApplication
from misc import di

app = QApplication(sys.argv)
window = di.Container.mainWindow()
window.init()
app.exec()
