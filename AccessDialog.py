import requests
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from RequestsHandler import RequestsHandler, RequestsHandlerException
from Settings import Settings

class AccessDialog(QDialog):

    ERROR_MESSAGE = 0
    DEFAULT_MESSAGE = 1

    def __init__(self, padre=None):
        super().__init__(padre)
        self.init_components()

    def init_components(self):
        self.setWindowTitle("Conceder permisos")
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setFixedWidth(320)
        self.setFixedHeight(440)
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
        self.messageLabel.setAlignment(Qt.AlignCenter)

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

    def sendRequest(self):
        message = ""
        if len(self.domainInput.text()) == 0:
            message += 'El campo "Dominio" es requerido\n'
        if len(self.usernameInput.text()) == 0:
            message += 'El campo "Nombre de usuario" es requerido\n'
        if len(self.passwordInput.text()) == 0:
            message += 'El campo "Contraseña" es requerido'
        if len(message) > 0:
            self.printMessage(message, self.ERROR_MESSAGE)
            return
        self.printMessage("Autenticando...")
        try:
            data = RequestsHandler.getAccessToken(self.usernameInput.text(), self.passwordInput.text(), self.domainInput.text())
            Settings.accessToken = data["access_token"]
            Settings.refreshToken = data["refresh_token"]
            Settings.accessTokenExpire = data["expires_in"]
            Settings.saveSettings()
            self.accept()
        except RequestsHandlerException as e:
            self.printMessage(e.message, self.ERROR_MESSAGE)

    def printMessage(self, string, message_type=DEFAULT_MESSAGE):
        self.messageLabel.setText(string)
        if message_type == self.DEFAULT_MESSAGE:
            self.messageLabel.setStyleSheet("font-size: 13px; color: #BDBDBD;")
        elif message_type == self.ERROR_MESSAGE:
            self.messageLabel.setStyleSheet("font-size: 13px; color: #F34335;")
        self.repaint()
