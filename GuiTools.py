from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QToolButton, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class HLayout(QHBoxLayout):

    def __init__(self, left_widget: QWidget, right_widget: QWidget, stretch=False, parent=None):
        super().__init__(parent)
        self.addWidget(left_widget)
        self.addWidget(right_widget)

        if stretch:
            self.addStretch()

class AlignedLabel(QLabel):

    def __init__(self, alignment: Qt.AlignmentFlag, string: str = "", parent=None):
        super().__init__(string, parent)
        self.setAlignment(alignment)

class StatusPanel(QFrame):

    def __init__(self, title: str, iconPath: str, parent=None):
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
        self.icon_label = AlignedLabel(Qt.AlignCenter)
        self.icon_label.setPixmap(QPixmap(iconPath))
        self.icon_label.setFixedHeight(60)
        self.title_label = AlignedLabel(Qt.AlignCenter, title)
        self.title_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        self.last_sync_label = InformationLabel(
            "Última sincronización exitosa:\n02:35pm 12-06-2018",
            InformationLabel.DATE)
        self.message = InformationLabel("", InformationLabel.DISABLE)

        self.layout.addSpacing(5)
        self.layout.addWidget(self.title_label)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.icon_label)
        self.layout.addSpacing(15)
        self.layout.addWidget(self.last_sync_label)
        self.layout.addWidget(self.message)
        self.layout.addStretch()

        self.message.set_message("Todo funciona correctamente", InformationLabel.SUCCESS)

    def change_message(self, string: str, message_type):
        if message_type == InformationLabel.DATE:
            self.last_sync_label.set_message(string, InformationLabel.DATE)
        else:
            self.message.set_message(string, message_type)

class InformationLabel(QWidget):

    SUCCESS = 0
    ERROR = 1
    WARNING = 2
    DATE = 3
    DISABLE = 4

    def __init__(self, string: str, message_type=SUCCESS, parent=None):
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
        self.layout.addStretch()

    def set_message(self, string: str = "", message_type=SUCCESS):
        self.icon_label.setPixmap(self.get_icon_pixmap(message_type))
        self.msg_label.setText(string)

    def get_icon_pixmap(self, message_type):
        if message_type == self.SUCCESS:
            return QPixmap("res/success_icon.png")
        elif message_type == self.ERROR:
            return QPixmap("res/error_icon.png")
        elif message_type == self.WARNING:
            return QPixmap("res/warning_icon.png")
        elif message_type == self.DATE:
            return QPixmap("res/date_icon.png")
        elif message_type == self.DISABLE:
            return QPixmap()

class ToolButton(QToolButton):

    def __init__(self, text="", icon=QIcon(), parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
