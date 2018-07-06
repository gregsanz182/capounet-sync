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
"""
Este módulo contiene la ventana principal del programa.
"""
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QPushButton, QMenu
from PyQt5.QtWidgets import QHBoxLayout, QTextEdit, QSystemTrayIcon, QAction, qApp
from PyQt5.QtGui import QPixmap, QIcon

import resources # pylint: disable=W0611
from settings import Settings
from options_dialog import OptionsDialog
from gui_tools import StatusPanel, QuestionDialog, AboutBox

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación.

    Para más informarción, leer la documentación de Qt5 'QMainWindow'.

    Note:
        La configuración de la aplicación debe haber sido cargada previamente. Para esto llamar
        a Settings.load_settings().

    Attributes:
        layout (QVBoxLayout): Layout del Widget central.
        socios_panel (StatusPanel): Panel que contiene información sobre la sincronización del
            archivo "Socios y Ahorros".
        prestamos_panel (StatusPanel): Panel que contiene información sobre la sincronización del
            archivo "Préstamos".
        text_log (QTextEdit): Campo de texto de solo lectura que muestra el log de los procesos
            llevados a cabo por el programa, asi como mensajes de advertencia y error.
        tray_icon (QSystemTrayIcon): Icono de en la bandeja del sistema.
    """

    def __init__(self):
        """Constructor de la clase. Construye e inicializa una instancia de MainWindow.

        Note:
            Antes de instanciar un objeto de esta clase, la configuración del programa debe haber
            sido cargada. Para esto llamar a Settings.load_settings().
        """
        super().__init__()
        self.setWindowTitle("CAPOUNET Sync")
        self.setFixedWidth(480)
        self.setFixedHeight(500)

        self.__init_components()

    def __init_components(self):
        """Inicializa los atributos de la clase y otros componentes del objeto.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        central_widget = QWidget()
        central_widget.setStyleSheet(Settings.global_style)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(":res/logo_2.png"))
        config_button = QPushButton("Ajustes")
        config_button.setObjectName("toolbar_button")
        config_button.setIcon(QIcon(":res/cog.png"))
        help_button = QPushButton("Ayuda")
        help_button.setObjectName("toolbar_button")
        help_button.setIcon(QIcon(":res/help.png"))
        help_menu = QMenu()
        logout_action = QAction("Cerrar sesión", self)
        logout_action.setIcon(QIcon(":res/logout.png"))
        logout_action.triggered.connect(self.__log_out)
        about_action = QAction("Acerca de", self)
        about_action.setIcon(QIcon(":res/about.png"))
        about_action.triggered.connect(self.__about)
        help_menu.addAction(logout_action)
        help_menu.addAction(about_action)
        help_button.setMenu(help_menu)
        top_layout.setContentsMargins(5, 6, 2, 6)
        top_layout.addWidget(logo_label)
        top_layout.addStretch()
        top_layout.addWidget(config_button)
        top_layout.addWidget(help_button)

        middle_layout = QHBoxLayout()
        self.socios_panel = StatusPanel("Socios y Ahorros", ":res/wallet.png")
        middle_layout.addWidget(self.socios_panel)
        self.prestamos_panel = StatusPanel("Préstamos", ":res/dues.png")
        middle_layout.addWidget(self.prestamos_panel)

        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)

        self.layout.addLayout(top_layout)
        self.layout.addLayout(middle_layout)
        self.layout.addWidget(self.text_log)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(Settings.sync_icon)
        show_action = QAction("Mostrar", self)
        show_action.setIcon(QIcon(":res/show.png"))
        quit_action = QAction("Salir", self)
        quit_action.setIcon(QIcon(":res/exit.png"))
        config_action = QAction("Preferencias", self)
        config_action.setIcon(QIcon(":res/cog.png"))
        show_action.triggered.connect(self.show)
        config_action.triggered.connect(self.open_options)
        quit_action.triggered.connect(self.close_app)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(config_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.show_now)

        config_button.clicked.connect(self.open_options)

    def open_options(self):
        """Abre el Dialog de opciones.
        """
        self.show()
        OptionsDialog.open_dialog(self)

    def __log_out(self):
        """Cierra sesión. Primero pregunta si desea cerrar sesión y luego procede.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        response = QuestionDialog.open_question(
            "¿Deas cerrar sesión?",
            "¿Realmente deseas cerrar sesión?. La sincronización se detendrá.",
            self
        )
        if response == 1:
            self.tray_icon.hide()
            self.hide()
            qApp.exit(1)

    def __about(self):
        """Muestra el dialogo de "Acerca de"

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        AboutBox.show_box(self)

    def print_log(self, string: str):
        """Imprime un mensaje en el log.

        El mensaje se mostrará con la fecha y hora del sistema en el momento en el que se llamó esta
        función.

        Args:
            string (str): Mensaje a mostrar.
        """
        flag = False
        if self.text_log.verticalScrollBar().value() == self.text_log.verticalScrollBar().maximum():
            flag = True
        self.text_log.insertHtml("<br><strong>>{}</strong>&nbsp;&nbsp;{}<br>".format(
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            string
        ))
        if flag:
            self.text_log.verticalScrollBar().setValue(self.text_log.verticalScrollBar().maximum())

    def closeEvent(self, event): # pylint: disable=C0103
        """Cierra la ventana. Pero no la aplicación.
        """
        event.ignore()
        self.hide()

    def show_now(self, reason: QSystemTrayIcon.ActivationReason):
        """Muestra la ventana cuando se hace doblo click en el icono de bandeja.
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def close_app(self):
        """Cierra completamente la aplicación.

        Primero se pregunta si se desea salir. Luego esconde el icono de bandeja y cierra la aplica-
        ción.
        """
        self.show()
        response = QuestionDialog.open_question("¿Deseas salir?", "¿Realmente deseas salir?", self)
        if response == 1:
            self.tray_icon.hide()
            qApp.quit()
        return
