from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QFileDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Settings import Settings
from GuiTools import HLayout

class OptionsDialog(QDialog):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setStyleSheet(Settings.global_style)
        self.__init_components()

    def __init_components(self):
        self.setFixedWidth(440)
        self.setFixedHeight(330)
        self.layout = QVBoxLayout(self)

        self.socios_check_box = QCheckBox()
        self.prestamos_check_box = QCheckBox()
        self.socios_path = QLineEdit()
        self.prestamos_path = QLineEdit()
        self.socios_button = QPushButton()
        self.prestamos_button = QPushButton()
        self.socios_button.setIcon(QIcon("res/search_icon.png"))
        self.socios_button.setStyleSheet("height: 18px; background-color: #232629;")
        self.prestamos_button.setIcon(QIcon("res/search_icon.png"))
        self.prestamos_button.setStyleSheet("height: 18px; background-color: #232629;")
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setObjectName("normal_button")
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.setObjectName("accept_button")

        self.__load_options()

        self.layout.addLayout(HLayout(
            self.socios_check_box,
            QLabel("Archivo de Socios y Ahorros"),
            True))
        self.layout.addLayout(HLayout(self.socios_path, self.socios_button))
        self.layout.addSpacing(2)
        self.layout.addLayout(HLayout(
            self.prestamos_check_box,
            QLabel("Archivo de Préstamos"),
            True))
        self.layout.addLayout(HLayout(self.prestamos_path, self.prestamos_button))
        self.layout.addStretch()
        self.layout.addLayout(HLayout(self.cancel_button, self.accept_button))
        self.setModal(True)

        self.__make_connections()

    def __load_options(self):
        self.socios_check_box.setCheckState(
            Qt.Checked if Settings.socios_file["enabled"] else Qt.Unchecked
        )
        self.prestamos_check_box.setCheckState(
            Qt.Checked if Settings.prestamos_file["enabled"] else Qt.Unchecked
        )
        self.prestamos_path.setText(Settings.prestamos_file["file_path"])
        self.socios_path.setText(Settings.socios_file["file_path"])

    def __make_connections(self):
        self.socios_button.clicked.connect(self.__select_socios_path)
        self.prestamos_button.clicked.connect(self.__select_prestamos_path)
        self.cancel_button.clicked.connect(self.reject)
        self.accept_button.clicked.connect(self.__save_state)

    def __select_socios_path(self):
        file_path = QFileDialog.getOpenFileName(
            self, "Selecciona archivo", filter="*.csv")[0]
        if file_path:
            self.socios_path.setText(file_path)

    def __select_prestamos_path(self):
        file_path = QFileDialog.getOpenFileName(
            self, "Selecciona archivo", filter="*.csv")[0]
        if file_path:
            self.prestamos_path.setText(file_path)

    def __save_state(self):
        Settings.socios_file.update({
            "enabled": True if self.socios_check_box.checkState() == Qt.Checked else False,
            "file_path": self.socios_path.text()
        })
        Settings.prestamos_file.update({
            "enabled": True if self.prestamos_check_box.checkState() == Qt.Checked else False,
            "file_path": self.prestamos_path.text()
        })
        Settings.save_settings()
        self.accept()

    @staticmethod
    def open_dialog(parent: QWidget = None) -> bool:
        dialog = OptionsDialog(parent)
        dialog.show()
        return dialog.exec_()
