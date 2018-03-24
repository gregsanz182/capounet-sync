import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSettings

class MainWindow(QMainWindow):

    def __init__(self, settings):
        super().__init__()
        self.setWindowTitle("CAPOUNET Sync")
        self.setFixedWidth(640)
        self.setFixedHeight(480)
        self.settings = settings