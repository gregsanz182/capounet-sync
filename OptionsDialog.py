from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QLabel, QHBoxLayout, QLineEdit, QToolButton, QPushButton
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from Settings import Settings

class OptionsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Settings.globalStyle)
        self.init_components()

    def init_components(self):
        self.setFixedWidth(440)
        self.setFixedHeight(330)
        self.layout = QVBoxLayout(self)

        self.sociosCheckbox = QCheckBox()
        self.prestamosCheckbox = QCheckBox()
        self.sociosPath = QLineEdit()
        self.prestamosPath = QLineEdit()
        self.sociosButton = QPushButton()
        self.prestamosButton = QPushButton()
        self.sociosButton.setIcon(QIcon("search_icon.png"))
        self.sociosButton.setStyleSheet("height: 18px; background-color: #232629;")
        self.prestamosButton.setIcon(QIcon("search_icon.png"))
        self.prestamosButton.setStyleSheet("height: 18px; background-color: #232629;")
        self.refreshCombo = QComboBox()
        self.refreshCombo.addItems(Settings.refreshOptions)
        self.refreshCombo.setItemDelegate(QStyledItemDelegate())
        self.cancelButton = QPushButton("Cancelar")
        self.cancelButton.setObjectName("normal_button")
        self.acceptButton = QPushButton("Aceptar")
        self.acceptButton.setObjectName("accept_button")

        self.layout.addLayout(HLayout(self.sociosCheckbox, QLabel("Archivo de Socios y Ahorros"), True))
        self.layout.addLayout(HLayout(self.sociosPath, self.sociosButton))
        self.layout.addSpacing(2)
        self.layout.addLayout(HLayout(self.prestamosCheckbox, QLabel("Archivo de Prestamos"), True))
        self.layout.addLayout(HLayout(self.prestamosPath, self.prestamosButton))
        self.layout.addSpacing(10)
        self.layout.addLayout(HLayout(QLabel("Tasa de refesco: "), self.refreshCombo, True))
        self.layout.addStretch()
        self.layout.addLayout(HLayout(self.cancelButton, self.acceptButton))
        self.setModal(True)

    @staticmethod
    def openDialog(parent = None):
        d = OptionsDialog(parent)
        d.show()
        d.exec_()

class HLayout(QHBoxLayout):

    def __init__(self, left_widget, right_widget, stretch=False, parent = None):
        super().__init__(parent)
        self.addWidget(left_widget)
        self.addWidget(right_widget)

        if stretch:
            self.addStretch()
