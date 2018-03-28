from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget, QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QIcon
from Settings import Settings
from OptionsDialog import OptionsDialog
from GuiTools import StatusPanel

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAPOUNET Sync")
        self.setFixedWidth(450)
        self.setFixedHeight(500)

        self.init_components()

    def init_components(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet(Settings.global_style)

        self.top_layout = QHBoxLayout()
        self.central_widget_layout.addLayout(self.top_layout)

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("res/logo_2.png"))
        self.config_button = QPushButton("Ajustes")
        self.config_button.setObjectName("normal_button")
        self.config_button.setStyleSheet("color: #B6B6B6; font-size: 12px;")
        self.config_button.setIcon(QIcon("res/cog.png"))
        self.top_layout.addSpacing(5)
        self.top_layout.addWidget(self.logo_label)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.config_button)

        self.middle_layout = QHBoxLayout()
        self.central_widget_layout.addLayout(self.middle_layout)

        self.socios_panel = StatusPanel("Socios y Ahorros", "res/wallet.png")
        self.middle_layout.addWidget(self.socios_panel)

        self.prestamos_panel = StatusPanel("Préstamos", "res/dues.png")
        self.middle_layout.addWidget(self.prestamos_panel)

        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        self.central_widget_layout.addWidget(self.text_log)

        self.__make_connections()

    def __make_connections(self):
        self.config_button.clicked.connect(self.open_options)

    def open_options(self):
        OptionsDialog.open_dialog(self)

    def print_log(self, string: str):
        flag = False
        if self.text_log.verticalScrollBar().value() == self.text_log.verticalScrollBar().maximum():
            flag = True
        self.text_log.insertHtml("<br><strong>>{}</strong>&nbsp;&nbsp;{}<br>".format(
            datetime.now().strftime("%d/%m/%Y %H:%M"),
            string
        ))
        if flag:
            self.text_log.verticalScrollBar().setValue(self.text_log.verticalScrollBar().maximum())

    def set_sync_state(self, string: str, message_type: int, status_panel: StatusPanel):
        status_panel.change_message(string, message_type)
