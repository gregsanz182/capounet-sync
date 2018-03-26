import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from Settings import Settings
from OptionsDialog import OptionsDialog
from GuiTools import AlignedLabel, InformationLabel, ToolButton

class MainWindow(QMainWindow):

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
        self.logoLabel.setPixmap(QPixmap("logo_2.png"))
        self.configButton = QPushButton("Ajustes")
        self.configButton.setObjectName("normal_button")
        self.configButton.setStyleSheet("color: #B6B6B6; font-size: 12px;")
        self.configButton.setIcon(QIcon("cog.png"))
        self.topLayout.addSpacing(5)
        self.topLayout.addWidget(self.logoLabel)
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.configButton)

        self.middleLayout = QHBoxLayout()
        self.centralWidgetLayout.addLayout(self.middleLayout)
        
        self.sociosPanel = StatusPanel("Socios y Ahorros", "wallet.png")
        self.middleLayout.addWidget(self.sociosPanel)

        self.prestamosPanel = StatusPanel("Prestamos", "dues.png")
        self.middleLayout.addWidget(self.prestamosPanel)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.centralWidgetLayout.addWidget(self.text)
        
class StatusPanel(QFrame):

    def __init__(self, title, iconPath, parent = None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame{
                background-color: #232629;
            }
            QFrame#status_panel{
                border: 1px solid #75787B;
                border-radius: 5px;
            }
        """)
        self.setObjectName("status_panel")
        self.setFixedHeight(275)

        self.layout = QVBoxLayout(self)
        self.iconLabel = AlignedLabel(Qt.AlignCenter)
        self.iconLabel.setPixmap(QPixmap(iconPath))
        self.iconLabel.setFixedHeight(60)
        self.titleLabel = AlignedLabel(Qt.AlignCenter, title)
        self.titleLabel.setStyleSheet("font-size: 13px; font-weight: bold;")
        self.lastSyncLabel = InformationLabel("Última sincronización exitosa:\n02:35pm 12-06-2018", InformationLabel.DATE)
        self.message = InformationLabel("", InformationLabel.DISABLE)

        self.layout.addSpacing(5)
        self.layout.addWidget(self.titleLabel)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.iconLabel)
        self.layout.addSpacing(15)
        self.layout.addWidget(self.lastSyncLabel)
        self.layout.addWidget(self.message)
        self.layout.addStretch()

        self.message.setMessage("Todo funciona correctamente", InformationLabel.SUCCESS)
