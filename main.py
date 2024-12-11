import sys
from PyQt6.QtWidgets import QApplication

import di as DI

app = QApplication(sys.argv)
window = DI.Container.mainWindow()
window.di_init()
app.exec()
