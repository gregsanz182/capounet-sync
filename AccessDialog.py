import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from RequestsHandler import RequestsHandler, RequestsHandlerException
from Settings import Settings

class AccessDialog(QDialog):

    def __init__(self, padre=None):
        super().__init__(padre)
        self.init_components()

    def init_components(self):
        self.setWindowTitle("Conceder permisos")
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setFixedWidth(320)
        self.labelLogo = QLabel()
        self.labelLogo.setPixmap(QPixmap("logo.png"))
        self.labelLogo.setAlignment(Qt.AlignCenter)
        self.domainLabel = QLabel("Dominio:")
        self.domainLabel.setStyleSheet("color: #BDBDBD;")
        self.usernameLabel = QLabel("Nombre de usuario:")
        self.usernameLabel.setStyleSheet("color: #BDBDBD;")
        self.passwordLabel = QLabel("Constraseña:")
        self.passwordLabel.setStyleSheet("color: #BDBDBD;")
        self.domainInput = QLineEdit("http://capounet.test")
        self.domainInput.setFixedHeight(30)
        self.domainInput.setStyleSheet("font-size: 13px;")
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
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setFixedHeight(60)

        self.layout.addSpacing(10)
        self.layout.addWidget(self.labelLogo)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.domainLabel)
        self.layout.addWidget(self.domainInput)
        self.layout.addWidget(self.usernameLabel)
        self.layout.addWidget(self.usernameInput)
        self.layout.addWidget(self.passwordLabel)
        self.layout.addWidget(self.passwordInput)
        self.layout.addWidget(self.messageLabel)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.botonAceptar)

        self.botonAceptar.clicked.connect(self.sendRequest)

    @staticmethod
    def obtainConfiguration():
        d = AccessDialog()
        d.show()
        d.exec_()
        return "hola"

    def sendRequest(self):
        try:
            data = RequestsHandler.getAccessToken(self.usernameInput.text(), self.passwordInput.text(), self.domainInput.text())
            Settings.accessToken = data["access_token"]
            Settings.refreshToken = data["refresh_token"]
            Settings.accessTokenExpire = data["expires_in"]
            Settings.saveSettings()
            self.close()
        except RequestsHandlerException as e:
            self.messageLabel.setText(e.message)
