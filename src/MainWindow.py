# -*- coding: utf-8 -*-
"""Este módulo contiene la ventana principal del programa."""

from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QPushButton, QMenu
from PyQt5.QtWidgets import QHBoxLayout, QTextEdit, QSystemTrayIcon, QAction, qApp
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from Settings import Settings
from OptionsDialog import OptionsDialog
from GuiTools import StatusPanel, QuestionDialog

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación.

    Para más informarción, leer la documentación de Qt5 'QMainWindow'.

    Note:
        La configuración de la aplicación debe haber sido cargada previamente. Para esto llamar
        a Settings.load_settings().

    Attributes:
        layout (QVBoxLayout): Layout del Widget central.
        top_layout (QHBoxLayout): Layout de la parte superior del widget central.
        middle_layout (QHBoxLayout): Layout para la mitad del widget central.
        config_button (QPushButton): Botón para acceder al Dialog de opciones.
        socios_panel (StatusPanel): Panel que contiene información sobre la sincronización del
            archivo "Socios y Ahorros".
        prestamos_panel (StatusPanel): Panel que contiene información sobre la sincronización del
            archivo "Préstamos".
        text_log (QTextEdit): Campo de texto de solo lectura que muestra el log de los procesos
            llevados a cabo por el programa, asi como mensajes de advertencia y error.
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

        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("res/logo_2.png"))
        self.config_button = QPushButton("Ajustes")
        self.config_button.setObjectName("normal_button")
        self.config_button.setStyleSheet("color: #B6B6B6; font-size: 12px;")
        self.config_button.setIcon(QIcon("res/cog.png"))
        self.top_layout.addSpacing(5)
        self.top_layout.addWidget(logo_label)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.config_button)

        self.middle_layout = QHBoxLayout()
        self.layout.addLayout(self.middle_layout)

        self.socios_panel = StatusPanel("Socios y Ahorros", "res/wallet.png")
        self.middle_layout.addWidget(self.socios_panel)

        self.prestamos_panel = StatusPanel("Préstamos", "res/dues.png")
        self.middle_layout.addWidget(self.prestamos_panel)

        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        self.layout.addWidget(self.text_log)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(Settings.sync_icon)
        show_action = QAction("Mostrar", self)
        quit_action = QAction("Salir", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.closeApp)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.show_now)

        self.config_button.clicked.connect(self.open_options)

    def open_options(self):
        """Abre el Dialog de opciones.
        """
        OptionsDialog.open_dialog(self)

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

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def show_now(self, reason: QSystemTrayIcon.ActivationReason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def closeApp(self):
        response = QuestionDialog.open_question("¿Deseas salir?", "¿Realmente deseas salir?", self)
        if response == QMessageBox.Accepted:
            self.tray_icon.hide()
            qApp.quit()
        return
