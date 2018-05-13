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
"""Este módulo incluye diferentes QWidgets y QLayouts personalizados para el uso en la aplicación
"""

import resources
from enum import Enum
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QFrame, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QPushButton, qApp
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap

class HLayout(QHBoxLayout):
    """QLayout horizontal para dos QWidgets. Hereda de QHBoxLayout."""

    def __init__(
            self, left_widget: QWidget, right_widget: QWidget,
            stretch: bool = False, parent: QWidget = None
        ):
        """Constructor de la clase. Construye e inicializa una instancia de HLayout.

        Args:
            left_widget (QWidget): QWidget que se ubicará en la izquierda del layout.
            right_widget (QWidget): QWidget que se ubicará en la izquierda del layout.
            stretch (bool, optional): Especifica si se añadirá un stretch (extensión) al final del
                layout. Defaults to None.
            parent (QWidget): QWidget padre del layout. El QWidget que utilizará este layout.
        """
        super().__init__(parent)
        self.addWidget(left_widget)
        self.addWidget(right_widget)

        if stretch:
            self.addStretch()

class AlignedLabel(QLabel):
    """QLabel alineado."""

    def __init__(self, alignment: Qt.AlignmentFlag, text: str = "", parent: QWidget = None):
        """Constructor de la clase. Construye e inicializa una instancia de AlignedLabel.

        Args:
            alignment (Qt.AligmentFlag): Alineación interna del QLabel. Ver Qt.AligmentFlag.
            text (str, optional): Texto que se mostrará en el QLabel.
            parent (QWidget, optional): Padre del QLabel. Defaults to None.
        """
        super().__init__(text, parent)
        self.setAlignment(alignment)

class MessageType(Enum):
    """Enumeración de los diferentes tipos de mensajes.

    Attributes:
        SUCCESS (int): Mensaje de éxito.
        ERROR (int): Mensaje de error.
        WARNING (int): Mensaje de advertencia.
        DATE (int): Mensaje que identifica un fecha.
        DISABLE (int): Mensaje desactivado.
    """

    SUCCESS = 0
    ERROR = 1
    WARNING = 2
    DATE = 3
    DISABLE = 4

class StatusPanel(QFrame):
    """QFrame que muestra el estado de sincronización de un archivo.

    Muestra información sobre un archivo a sincronizar, tal como la última fecha de sincronización
    exitosa, mensajes de error y mensajes de advertencia.

    Attributes:
        layout (QVBoxLayout): Layout del panel.
        title_label (AlignedLabel): Label que muestra el titulo del archivo a sincronizar.
        last_sync_label (InformationLabel): Label encargado de mostrar la última sincronización.
        message_label (InformationLabel): Label encargado de mostrar un mensaje sobre el estado
            actual de la sincronización asi como también un mensaje de error o de emergencia.
    """
    def __init__(self, title: str, icon_path: str, parent: QWidget = None):
        """Constructor de la clase. Construye e inicializa una instancia de StatusPanel.

        Args:
            title (str): Título del panel. Especificamente el título del archivo que se sincroniza.
            icon_path (str): Ruta del icono que se mostrará en el panel.
            parent (QWidget): Padre del panel. Defaults to None.
        """
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
        icon_label = AlignedLabel(Qt.AlignCenter)
        icon_label.setPixmap(QPixmap(icon_path))
        icon_label.setFixedHeight(60)
        self.title_label = AlignedLabel(Qt.AlignCenter, title)
        self.title_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        self.last_sync_label = InformationLabel(
            "Última sincronización exitosa:",
            MessageType.DATE
        )
        self.message_label = InformationLabel("", MessageType.DISABLE)

        self.layout.addSpacing(5)
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(5)
        self.layout.addWidget(icon_label)
        self.layout.addSpacing(15)
        self.layout.addWidget(self.last_sync_label)
        self.layout.addWidget(self.message_label)
        self.layout.addStretch()

        self.message_label.set_message("Todo funciona correctamente", MessageType.SUCCESS)

    def change_message(self, string: str, message_type: MessageType):
        """Cambia los mensajes que muestra el panel.

        Args:
            string (str): Texto a mostrar. Si message_type es DATE, este parametro debería ser una
                fecha en str con el formato de preferencia. Se recomienda '%H:%M %d-%m-%Y'.
            message_type (MessageType): Tipo de mensaje. Si es igual a MessageType.DATE, entonces
                se cambiará la fecha de la última sincronización.
        """
        if message_type == MessageType.DATE:
            #Si el tipo de mensaje es DATE se cambia el mensaje de last_sync_label
            self.last_sync_label.set_message(
                "Última sincronización exitosa:<br>{}".format(string),
                MessageType.DATE
            )
        else:
            #Caso contrario se cambia el texto de message_label
            self.message_label.set_message(string, message_type)

class InformationLabel(QWidget):
    """Label que muestra información sobre la sincronización en un StatusPanel.

    Este QWidget consiste de dos QLabel. Uno muestra un icono dependiendo el tipo de mensaje, y otro
    que muestra un texto personalizado.

    Attributes:
        layout (QHBoxLayout): Layout de este QWidget personalizado.
        icon_label (QLabel): Label que muestra el icono del mensaje dependiendo del MessageType.
        msg_label (QLabel): Label que muestra el texto del mensaje.
    """

    def __init__(
            self, string: str, message_type: MessageType = MessageType.SUCCESS,
            parent: QWidget = None
        ):
        """Constructor de la clase. Construye e inicializa una instancia de InformationLabel.

        Args:
            string (str): Texto a mostrar.
            message_type (MessageType): Tipo del mensaje. Defaults to MessageType.SUCCESS.
            parent (QWidget): Padre del label. Defaults to None.
        """
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(QSize(13, 13))
        self.icon_label.setPixmap(self.get_icon_pixmap(message_type))

        self.msg_label = QLabel(string)
        self.msg_label.setWordWrap(True)

        self.layout.addWidget(self.icon_label)
        self.layout.setAlignment(self.icon_label, Qt.AlignTop)
        self.layout.addSpacing(7)
        self.layout.addWidget(self.msg_label)

    def set_message(self, string: str = "", message_type: MessageType = MessageType.SUCCESS):
        """Cambia el mensaje del InformationLabel

        Args:
            string (str): Texto del mensaje.
            message_type (MessageType): Tipo de mensaje. Defaults to None
        """
        self.icon_label.setPixmap(self.get_icon_pixmap(message_type))
        self.msg_label.setText(string)

    @staticmethod
    def get_icon_pixmap(message_type: MessageType) -> QPixmap:
        """Obtiene el QPixmap del icono que representa el tipo de mensaje.

        Args:
            message_type (MessageType): Tipo de mensaje.

        Returns:
            QPixmap: El QPixmap que representa el tipo de mensaje.
        """
        if message_type == MessageType.SUCCESS:
            return QPixmap(":res/success_icon.png")
        elif message_type == MessageType.ERROR:
            return QPixmap(":res/error_icon.png")
        elif message_type == MessageType.WARNING:
            return QPixmap(":res/warning_icon.png")
        elif message_type == MessageType.DATE:
            return QPixmap(":res/date_icon.png")
        elif message_type == MessageType.DISABLE:
            return QPixmap()

class QuestionDialog(QMessageBox):

    def __init__(self, title: str, text: str, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setText(text)

        yes_button = QPushButton("Sí")
        yes_button.setFixedWidth(100)
        no_button = QPushButton("No")
        no_button.setFixedWidth(100)
        self.addButton(no_button, QMessageBox.NoRole)
        self.addButton(yes_button, QMessageBox.YesRole)
        self.setDefaultButton(no_button)
        self.setIcon(QMessageBox.Question)

    @staticmethod
    def open_question(title: str, text: str, parent: QWidget = None):
        dialog = QuestionDialog(title, text, parent)
        return dialog.exec_()

class AboutBox(QMessageBox):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setTextFormat(Qt.RichText)
        self.setText(
            """
<style>
    a {color: #eeeeef;}
    div {color: #ececec;}
</style>
<div>
<strong>CAPOUNET Sync</strong>
<br>©2018
<br><br>
Desarrollado para la Caja de Ahorros del Personal Obrero de la Universidad \
Nacional Experimental del Táchira.
<br><br>
<strong>Esta aplicación ha sido desarrollada con:</strong>
<br> - Python 3.6
<br> - PyQt5
<br> - Requests 2.18.4
<br> - QDarkStyle 2.5.4
<br><br>
<strong>Desarrolladores:</strong>
<br> -Gregory Sánchez <a href="https://github.com/gregsanz182">@gregsanz182</a>
<br> -Anny Chacón <a href="https://github.com/AnnyEsme27">@AnnyEsme27</a>
<br>
<br><strong>GNU General Public License v3.0</strong>
<br>Este programa no incluye garantía alguna.
<br>Es software libre, y puedes distribuirlo bajo ciertas condiciones.
<br>Debiste haber recibido una copia de la Licencia Pública General (GNU) con este programa.
Si no es así, visita <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>.
</div>
            """
        )
        self.setIconPixmap(qApp.windowIcon().pixmap(QSize(80, 80)))
        self.setWindowTitle("Sobre CAPOUNET Sync")

    @classmethod
    def show_box(cls, parent: QWidget = None):
        box = AboutBox(parent)
        box.exec_()
