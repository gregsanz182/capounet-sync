from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from RequestsHandler import RequestsHandler, RequestsHandlerException
from Settings import Settings

class AccessDialog(QDialog):

    ERROR_MESSAGE = 0
    DEFAULT_MESSAGE = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_components()

    def init_components(self):
        self.setWindowTitle("Conceder permisos")
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setFixedWidth(320)
        self.setFixedHeight(440)
        self.setStyleSheet(Settings.globalStyle)
        self.label_logo = QLabel()
        self.label_logo.setPixmap(QPixmap("res/logo.png"))
        self.label_logo.setAlignment(Qt.AlignCenter)
        self.domain_input = QLineEdit("http://capounet.test")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.setFixedHeight(40)
        self.boton_aceptar.setObjectName("accept_button")
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFixedHeight(60)

        self.layout.addSpacing(10)
        self.layout.addWidget(self.label_logo)
        self.layout.addSpacing(20)
        self.layout.addWidget(QLabel("Dominio:"))
        self.layout.addWidget(self.domain_input)
        self.layout.addWidget(QLabel("Nombre de usuario:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Constraseña:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.message_label)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.boton_aceptar)

        self.boton_aceptar.clicked.connect(self.send_request)

    @staticmethod
    def obtain_configuration():
        dialog = AccessDialog()
        dialog.show()
        return dialog.exec_()

    def send_request(self):
        message = ""
        if not self.domain_input.text():
            message += 'El campo "Dominio" es requerido\n'
        if not self.username_input.text():
            message += 'El campo "Nombre de usuario" es requerido\n'
        if not self.password_input.text():
            message += 'El campo "Contraseña" es requerido'
        if message:
            self.print_message(message, self.ERROR_MESSAGE)
            return
        self.print_message("Autenticando...")
        try:
            data = RequestsHandler.getAccessToken(
                self.username_input.text(),
                self.password_input.text(),
                self.domain_input.text()
            )
            Settings.accessToken = data["access_token"]
            Settings.refreshToken = data["refresh_token"]
            Settings.accessTokenExpire = data["expires_in"]
            Settings.saveSettings()
            self.accept()
        except RequestsHandlerException as exception:
            self.print_message(exception.message, self.ERROR_MESSAGE)

    def print_message(self, string, message_type=DEFAULT_MESSAGE):
        self.message_label.setText(string)
        if message_type == self.DEFAULT_MESSAGE:
            self.message_label.setStyleSheet("font-size: 13px; color: #BDBDBD;")
        elif message_type == self.ERROR_MESSAGE:
            self.message_label.setStyleSheet("font-size: 13px; color: #F34335;")
        self.repaint()
