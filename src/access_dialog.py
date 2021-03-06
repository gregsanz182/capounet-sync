# -*- coding: utf-8 -*-
# This file is part of CAPOUNET Sync.
#
# CAPOUNET Sync
# Copyright (C) 2018  Gregory Sánchez and Anny Chacón
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Este módulo incluye AccessDialog, un QDialog para el manejo de las credenciales de usuario.

El AccessDialog pregunta las credenciales de usuario y obtiene los tokens de acceso y de refresco
necesarios para la el manejo de la API rest.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import resources # pylint: disable=W0611
from request_handler import RequestsHandler, RequestsHandlerException
from settings import Settings

class AccessDialog(QDialog):
    """QDialog para la obtención de las credenciales de usuario y la petición de tokens.

    Proporciona QLineEdit para el 'username', 'password' y 'dominio'.
    También realiza la petición al servidor API y obtiene los tokens de acceso y refresco.

    Para abrir este QDialog basta con llamar a AccessDialog.obtain_configuration().

    Note:
        La configuración de la aplicación debe haber sido cargada previamente. Para esto llamar
        a Settings.load_settings().

    Attributes:
        layout (QVBoxLayout): Layout que contendrá los widgets de este QDialog.
        domain_input (QLineEdit): Permite el ingreso del dominio de la API.
        username_input (QLineEdit): Permite el ingreso del nombre de usuario.
        password_input (QLineEdit): Permite el ingreso de la contraseña del usuario.
        accept_button (QPushButton): Botón para aceptar el formulario y enviar la petición.
        message_label (QLabel): Muestra los mensajes al usuario.
    """

    ERROR_MESSAGE = 0 #Identifica un mensaje de error
    DEFAULT_MESSAGE = 1 #Identifica un mensaje normal

    def __init__(self, parent: QWidget = None):
        """Constructor de la clase. Construye e inicializa una instancia de AccessDialog.

        Note:
            Antes de instanciar un objeto de esta clase, la configuración del programa debe haber
            sido cargada. Para esto llamar a Settings.load_settings().

        Args:
            parent (QWidget): Padre de este QDialog. Defaults to None.
        """
        super().__init__(parent)
        self.__init_components()

    def __init_components(self):
        """Inicializa los atributos de la clase y otros componentes del objeto.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        #Atributos del dialogo
        self.setWindowTitle("Conceder permisos")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedWidth(320)
        self.setStyleSheet(Settings.global_style)

        #Asignación del QLayout contenedor
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        #Logo de la aplicación
        label_logo = QLabel()
        label_logo.setPixmap(QPixmap(":res/logo.png"))
        label_logo.setAlignment(Qt.AlignCenter)

        #QLineEdit para 'usuario', 'contraseña' y 'dominio'
        self.domain_input = QLineEdit("http://capounet.unet.edu.ve")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        #QLabel en donde se mostrarán los mensajes de error y advertencia
        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFixedHeight(60)

        #QPushButton 'Aceptar'
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.setFixedHeight(40)
        self.accept_button.setObjectName("accept_button")

        #Inserción de items en el layout del QDialog
        self.layout.addSpacing(10)
        self.layout.addWidget(label_logo)
        self.layout.addSpacing(20)
        self.layout.addWidget(QLabel("Dominio:"))
        self.layout.addWidget(self.domain_input)
        self.layout.addWidget(QLabel("Correo de administrador:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Constraseña:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.message_label)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.accept_button)

        self.setFixedSize(self.size())

        self.accept_button.clicked.connect(self.__send_request)

    @staticmethod
    def obtain_configuration() -> int:
        """Abre un AccessDialog para su uso rápido.

        Crea un objeto instancia de AccessDialog y a la vez abre el Dialog.

        Note:
            Puede ser llamado sin necesidad de instanciar un objeto previamente.

        Returns:
            int: 1 si la obtención de los tokens fue exitosa, 0 si se canceló el dialog
                (Por medio del botón 'Salir' de la ventana).
        """
        dialog = AccessDialog()
        dialog.show()
        return dialog.exec_()

    def __send_request(self):
        """Envia la petición al servidor para obtener los tokens.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
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
            self.accept()
        except RequestsHandlerException as exception:
            self.print_message(exception.message, self.ERROR_MESSAGE)

    def print_message(self, string: str, message_type: int = DEFAULT_MESSAGE):
        """Imprime un mensaje en el message_label.

        Imprime el 'string' que recibe como parametro, con el tipo de mensaje especificado
        en 'message_type'.

        Args:
            string (str): Mensaje a mostrar.
            message_type (int): Tipo de mensaje. Este puede ser normal o de error. Corresponde
            a las constantes DEFAULT_MESSAGE y ERROR_MESSAGE respectivamente. Un ERROR_MESSAGE
            se muestra de color rojo.
        """
        self.message_label.setText(string)
        if message_type == self.DEFAULT_MESSAGE:
            self.message_label.setStyleSheet("font-size: 13px; color: #BDBDBD;")
        elif message_type == self.ERROR_MESSAGE:
            self.message_label.setStyleSheet("font-size: 13px; color: #F34335;")
        self.repaint()
