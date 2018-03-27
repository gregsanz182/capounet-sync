import sys
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QTextEdit, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from Settings import Settings
from OptionsDialog import OptionsDialog
from GuiTools import AlignedLabel, InformationLabel, ToolButton, StatusPanel

class MainWindow(QMainWindow):

    printLogSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAPOUNET Sync")
        self.setFixedWidth(450)
        self.setFixedHeight(500)

        self.init_components()

    def init_components(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidgetLayout = QVBoxLayout(self.centralWidget)
        self.centralWidget.setStyleSheet(Settings.globalStyle)

        self.topLayout = QHBoxLayout()
        self.centralWidgetLayout.addLayout(self.topLayout)
        
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(QPixmap("res/logo_2.png"))
        self.configButton = QPushButton("Ajustes")
        self.configButton.setObjectName("normal_button")
        self.configButton.setStyleSheet("color: #B6B6B6; font-size: 12px;")
        self.configButton.setIcon(QIcon("res/cog.png"))
        self.topLayout.addSpacing(5)
        self.topLayout.addWidget(self.logoLabel)
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.configButton)

        self.middleLayout = QHBoxLayout()
        self.centralWidgetLayout.addLayout(self.middleLayout)
        
        self.sociosPanel = StatusPanel("Socios y Ahorros", "res/wallet.png")
        self.middleLayout.addWidget(self.sociosPanel)

        self.prestamosPanel = StatusPanel("Prestamos", "res/dues.png")
        self.middleLayout.addWidget(self.prestamosPanel)

        self.textLog = QTextEdit()
        self.textLog.setReadOnly(True)
        self.centralWidgetLayout.addWidget(self.textLog)

        self.makeConnections()

    def makeConnections(self):
        self.configButton.clicked.connect(self.openOptions)
        self.printLogSignal.connect(self.printLog)

    def openOptions(self):
        OptionsDialog.openDialog(self)

    def printLog(self, string: str):
        flag = False
        if self.textLog.verticalScrollBar().value() == self.textLog.verticalScrollBar().maximum():
            flag = True
        self.textLog.insertPlainText("\n>> {}   {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M"), string))
        if flag:
            self.textLog.verticalScrollBar().setValue(self.textLog.verticalScrollBar().maximum())

