"""Este módulo contiene la clase AccessDialog, encargada de presentar un QDialog que permita 
obtener los tokens necesarios para el uso de la API por medio de las credenciales de usuario."""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from RequestsHandler import RequestsHandler, RequestsHandlerException
from Settings import Settings

class AccessDialog(QDialog):
    """QDialog para el acceso a la aplicación. Proporciona QLineEdit para el 'username', 'password'
    y 'dominio'. También realiza la petición al servidor y obtiene los tokens de acceso y refresco.
    """

    ERROR_MESSAGE = 0
    DEFAULT_MESSAGE = 1

    def __init__(self, parent: QWidget = None):
        """Inicializa el objeto.
        Settings.load_settings() debe haber sido llamado previamente.
        
        :param string: str: 
        """
        super().__init__(parent)
        self.init_components()

    def init_components(self):
        """Inicializa todos los componentes del QDialog"""
        #Atributos del dialogo
        self.setWindowTitle("Conceder permisos")
        self.setFixedWidth(320)
        self.setFixedHeight(440)
        self.setStyleSheet(Settings.global_style)

        #Asignación del QLayout contenedor
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        #Logo de la aplicación
        label_logo = QLabel()
        label_logo.setPixmap(QPixmap("res/logo.png"))
        label_logo.setAlignment(Qt.AlignCenter)

        #QLineEdit para 'usuario', 'contraseña' y 'dominio'
        self.domain_input = QLineEdit("http://capounet.test")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        #QLabel en donde se mostrarán los mensajes de error y advertencia
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFixedHeight(60)

        #QPushButton 'Aceptar'
        self.boton_aceptar = QPushButton("Aceptar")
        self.boton_aceptar.setFixedHeight(40)
        self.boton_aceptar.setObjectName("accept_button")

        #Inserción de items en el layout del QDialog
        self.layout.addSpacing(10)
        self.layout.addWidget(label_logo)
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
    def obtain_configuration() -> bool:
        """Crea un AccessDialog, realiza la petición de tokens y los guarda en Settings.
        Devuelve True si se obtuvó los tokens, False si se cancelo el QDialog.
        Settings.load_settings() debe haber sido llamado previamente."""
        dialog = AccessDialog()
        dialog.show()
        return dialog.exec_()

    def send_request(self):
        """Envia la petición al servidor para obtener los tokens"""
        message = ""
        #Verifica si todos los QLineEdit han sido llenados.
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
            #Realiza la petición y guarda los tokens. Si ocurre una excepción, imprime el mensaje.
            data = RequestsHandler.get_access_token(
                self.username_input.text(),
                self.password_input.text(),
                self.domain_input.text()
            )
            #Guarda en Settings los datos obtenidos
            Settings.access_token = data["access_token"]
            Settings.refresh_token = data["refresh_token"]
            Settings.access_token_expire = data["expires_in"]
            Settings.save_settings()
            self.accept()
        except RequestsHandlerException as exception:
            self.print_message(exception.message, self.ERROR_MESSAGE)

    def print_message(self, string: str, message_type: int = DEFAULT_MESSAGE):
        """Imprime el 'string' que recibe como parametro, con el tipo de mensaje especificado
        en 'message_type'"""
        self.message_label.setText(string)
        if message_type == self.DEFAULT_MESSAGE:
            self.message_label.setStyleSheet("font-size: 13px; color: #BDBDBD;")
        elif message_type == self.ERROR_MESSAGE:
            self.message_label.setStyleSheet("font-size: 13px; color: #F34335;")
        self.repaint()
