from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Settings import Settings
from GuiTools import HLayout

class OptionsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Settings.global_style)
        self.init_components()

    def init_components(self):
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
        self.refresh_combo = QComboBox()
        self.refresh_combo.addItems(Settings.refresh_options)
        self.refresh_combo.setItemDelegate(QStyledItemDelegate())
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setObjectName("normal_button")
        self.accept_button = QPushButton("Aceptar")
        self.accept_button.setObjectName("accept_button")

        self.load_options()

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
        self.layout.addSpacing(10)
        self.layout.addLayout(HLayout(QLabel("Tasa de refesco: "), self.refresh_combo, True))
        self.layout.addStretch()
        self.layout.addLayout(HLayout(self.cancel_button, self.accept_button))
        self.setModal(True)

        self.make_connections()

    def load_options(self):
        self.socios_check_box.setCheckState(
            Qt.Checked if Settings.socios_file["enabled"] else Qt.Unchecked
        )
        self.prestamos_check_box.setCheckState(
            Qt.Checked if Settings.prestamos_file["enabled"] else Qt.Unchecked
        )
        self.prestamos_path.setText(Settings.prestamos_file["file_path"])
        self.socios_path.setText(Settings.socios_file["file_path"])
        self.refresh_combo.setCurrentIndex(Settings.refresh_rate)

    def make_connections(self):
        self.socios_button.clicked.connect(self.select_socios_path)
        self.prestamos_button.clicked.connect(self.select_prestamos_path)
        self.cancel_button.clicked.connect(self.reject)
        self.accept_button.clicked.connect(self.save_state)

    def select_socios_path(self):
        self.socios_path.setText(QFileDialog.getOpenFileName(
            self, "Selecciona archivo", filter="*.csv *.json")[0])

    def select_prestamos_path(self):
        self.prestamos_path.setText(QFileDialog.getOpenFileName(
            self,
            "Selecciona archivo",
            filter="*.csv *.json")[0])

    def save_state(self):
        Settings.socios_file.update({
            "enabled": True if self.socios_check_box.checkState() == Qt.Checked else False,
            "file_path": self.socios_path.text()
        })
        Settings.prestamos_file.update({
            "enabled": True if self.prestamos_check_box.checkState() == Qt.Checked else False,
            "file_path": self.prestamos_path.text()
        })
        Settings.refresh_rate = self.refresh_combo.currentIndex()
        Settings.save_settings()
        self.accept()

    @staticmethod
    def open_dialog(parent=None):
        dialog = OptionsDialog(parent)
        dialog.show()
        return dialog.exec_()
