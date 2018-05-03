# -*- coding: utf-8 -*-
"""Este módulo provee un Dialog para representar las diferentes opciones de la aplicación."""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Settings import Settings
from GuiTools import HLayout

class OptionsDialog(QDialog):
    """Dialog que proporciona inputs para la configuración del programa.

    Provee una interfaz gráfica para configurar las rutas de los archivos a sincronizar y otras
    preferencias. Una vez se han seleccionado las preferencias, el Dialog guarda en Settings las
    configuraciones.

    Para abrir este QDialog basta con llamar a OptionsDialog.open_dialog().

    Note:
        La configuración de la aplicación debe haber sido cargada previamente. Para esto llamar
        a Settings.load_settings()

    Attributes:
        layout (QVBoxLayout): Layout del dialog.
        socios_check_box (QCheckBox): Checkbox para habilitar o deshabilitar la sincronización del
            archivo 'Socios y Ahorros'.
        prestamos_check_box (QCheckBox): Checkbox para habilitar o deshabilitar la sincronización
            del archivo 'Prestamos'.
        socios_path (QLineEdit): Permite el ingreso de la ruta al archivo 'Socios y Ahorros'.
        prestamos_path (QLineEdit): Permite el ingreso de la ruta al archivo 'Prestamos'.
    """

    def __init__(self, parent: QWidget = None):
        """Constructor de la clase. Construye e inicializa una instancia de OptionsDialog.

        Note:
            Antes de instanciar un objeto de esta clase, la configuración del programa debe haber
            sido cargada. Para esto llamar a Settings.load_settings().

        Args:
            parent (QWidget): Padre de este QDialog. Defaults to None.
        """
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet(Settings.global_style)
        self.__init_components()

    def __init_components(self):
        """Inicializa los atributos de la clase y otros componentes del objeto.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        self.setFixedWidth(440)
        self.setFixedHeight(330)
        self.layout = QVBoxLayout(self)

        self.socios_check_box = QCheckBox()
        self.prestamos_check_box = QCheckBox()
        self.socios_path = QLineEdit()
        self.prestamos_path = QLineEdit()
        socios_button = QPushButton()
        prestamos_button = QPushButton()
        socios_button.setIcon(QIcon("res/search_icon.png"))
        socios_button.setStyleSheet("height: 18px; background-color: #232629;")
        prestamos_button.setIcon(QIcon("res/search_icon.png"))
        prestamos_button.setStyleSheet("height: 18px; background-color: #232629;")
        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("normal_button")
        accept_button = QPushButton("Aceptar")
        accept_button.setObjectName("accept_button")

        self.__load_options()
        self.layout.addLayout(HLayout(
            self.socios_check_box,
            QLabel("Archivo de Socios y Ahorros"),
            True))
        self.layout.addLayout(HLayout(self.socios_path, socios_button))
        self.layout.addSpacing(2)
        self.layout.addLayout(HLayout(
            self.prestamos_check_box,
            QLabel("Archivo de Préstamos"),
            True))
        self.layout.addLayout(HLayout(self.prestamos_path, prestamos_button))
        self.layout.addStretch()
        self.layout.addLayout(HLayout(cancel_button, accept_button))
        self.setModal(True)

        socios_button.clicked.connect(self.__select_socios_path)
        prestamos_button.clicked.connect(self.__select_prestamos_path)
        cancel_button.clicked.connect(self.reject)
        accept_button.clicked.connect(self.__save_state)

    def __load_options(self):
        """Carga el estado inicial de los componentes dependiendo de las preferencias cargadas en el
        Settings.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        self.socios_check_box.setCheckState(
            Qt.Checked if Settings.socios_file["enabled"] else Qt.Unchecked
        )
        self.prestamos_check_box.setCheckState(
            Qt.Checked if Settings.prestamos_file["enabled"] else Qt.Unchecked
        )
        self.prestamos_path.setText(Settings.prestamos_file["file_path"])
        self.socios_path.setText(Settings.socios_file["file_path"])

    def __select_socios_path(self):
        """Abre una ventana para seleccionar el archivo de "Socios y Ahorros".

        Abre una ventana para seleccionar un archivo y guarda su ruta en socios_path.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        file_path = QFileDialog.getOpenFileName(
            self, "Selecciona archivo", filter="*.csv")[0]
        if file_path:
            self.socios_path.setText(file_path)
            self.socios_check_box.setCheckState(Qt.Checked)

    def __select_prestamos_path(self):
        """Abre una ventana para seleccionar el archivo de "Prestamos".

        Abre una ventana para seleccionar un archivo y guarda su ruta en prestamos_path.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        file_path = QFileDialog.getOpenFileName(
            self, "Selecciona archivo", filter="*.csv")[0]
        if file_path:
            self.prestamos_path.setText(file_path)

    def __save_state(self):
        """Guarda las preferencias configuradas en el Dialog.

        Note:
            Esta función no debe ser llamada desde el exterior, puesto que su uso es interno en la
            clase.
        """
        Settings.socios_file.update({
            "enabled": True if self.socios_check_box.checkState() == Qt.Checked \
            and self.socios_path.text() else False,
            "file_path": self.socios_path.text()
        })
        Settings.prestamos_file.update({
            "enabled": True if self.prestamos_check_box.checkState() == Qt.Checked \
            and self.prestamos_path.text() else False,
            "file_path": self.prestamos_path.text()
        })
        Settings.save_settings()
        self.accept()

    @staticmethod
    def open_dialog(parent: QWidget = None) -> int:
        """Abre un OptionsDialog para su uso rápido.

        Crea un objeto instancia de OptionsDialog y a la vez abre el Dialog.

        Note:
            Puede ser llamado sin necesidad de instanciar un objeto previamente.

        Args:
            parent (QWidget): Padre de este QDialog. Defaults to None.

        Returns:
            int: 1 si se guardó la configuración a través del botón 'Aceptar', 0 si se canceló el
            dialog (Por medio del botón 'Salir' de la ventana o a través del botón 'Cancelar').
        """
        dialog = OptionsDialog(parent)
        dialog.show()
        return dialog.exec_()
