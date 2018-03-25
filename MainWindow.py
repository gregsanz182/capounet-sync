import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import QSettings
from Settings import Settings
from OptionsDialog import OptionsDialog

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAPOUNET Sync")
        self.setFixedWidth(320)

        self.init_components()

    def init_components(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidgetLayout = QVBoxLayout(self.centralWidget)
        self.centralWidget.setStyleSheet(Settings.globalStyle)

        self.centralWidgetLayout.addWidget(QLabel("hola"))
        self.centralWidgetLayout.addWidget(QLineEdit(""))
        self.centralWidgetLayout.addWidget(QLineEdit(""))
        self.centralWidgetLayout.addWidget(QPushButton("LALALALAL"))
        