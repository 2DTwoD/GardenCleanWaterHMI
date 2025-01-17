from PyQt6.QtCore import QTimer


class Updater:

    def __init__(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.startUpdate)
        self.timer.daemon = True

    def startUpdate(self):
        self.updateAction()
        self.timer.start()

    def stopUpdate(self):
        self.timer.stop()

    def updateAction(self):
        pass
