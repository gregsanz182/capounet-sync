import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class AccessDialog(QDialog):

    def __init__(self, settings, padre=None):
        super().__init__(padre)
        self.settings = settings
        self.init_components()

    def init_components(self):
        self.setWindowTitle("Conceder permisos")
        self.layout = QVBoxLayout(self)
        self.setFixedWidth(320)
        self.setModal(True)
        self.labelLogo = QLabel()
        self.labelLogo.setPixmap(QPixmap("logo.png"))
        self.labelLogo.setAlignment(Qt.AlignCenter)
        self.usernameLabel = QLabel("Nombre de usuario:")
        self.usernameLabel.setStyleSheet("color: #BDBDBD;")
        self.passwordLabel = QLabel("Constraseña:")
        self.passwordLabel.setStyleSheet("color: #BDBDBD;")
        self.usernameInput = QLineEdit()
        self.usernameInput.setFixedHeight(30)
        self.usernameInput.setStyleSheet("font-size: 13px;")
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedHeight(30)
        self.passwordInput.setStyleSheet("font-size: 13px;")
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.botonAceptar = QPushButton("Aceptar")
        self.botonAceptar.setFixedHeight(40)
        self.messageLabel = QLabel("")
        self.messageLabel.setStyleSheet("font-size: 13px; color: #F34335;")

        self.layout.addSpacing(10)
        self.layout.addWidget(self.labelLogo)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.usernameLabel)
        self.layout.addWidget(self.usernameInput)
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.passwordInput)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.messageLabel)
        self.layout.addSpacing(30)
        self.layout.addWidget(self.botonAceptar)

        self.botonAceptar.clicked.connect(self.sendRequest)

    @staticmethod
    def getTokens(settings):
        d = AccessDialog(settings)
        d.show()
        d.exec_()
        return "hola"

    def sendRequest(self):
        pass
