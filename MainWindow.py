import sys
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAPOUNET Sync")
        self.setFixedWidth(640)
        self.setFixedHeight(480)

        
