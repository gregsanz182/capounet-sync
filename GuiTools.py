from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QToolButton, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon

class HLayout(QHBoxLayout):

    def __init__(self, left_widget, right_widget, stretch=False, parent = None):
        super().__init__(parent)
        self.addWidget(left_widget)
        self.addWidget(right_widget)

        if stretch:
            self.addStretch()

class AlignedLabel(QLabel):

    def __init__(self, alignment: Qt.AlignmentFlag, string: str = "", parent = None):
        super().__init__(string, parent)
        self.setAlignment(alignment)

class InformationLabel(QWidget):

    SUCCESS = 0
    ERROR = 1
    WARNING = 2
    DATE = 3
    DISABLE = 4

    def __init__(self, string: str, message_type = SUCCESS, parent = None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.iconLabel = QLabel()
        self.iconLabel.setFixedSize(QSize(13, 13))
        self.iconLabel.setPixmap(self.getIconPixmap(message_type))

        self.msgLabel = QLabel(string)
        self.msgLabel.setWordWrap(True)

        self.layout.addWidget(self.iconLabel)
        self.layout.setAlignment(self.iconLabel, Qt.AlignTop)
        self.layout.addSpacing(7)
        self.layout.addWidget(self.msgLabel)
        self.layout.addStretch()

    def setMessage(self, string: str="", message_type = SUCCESS):
        self.iconLabel.setPixmap(self.getIconPixmap(message_type))
        self.msgLabel.setText(string)

    def getIconPixmap(self, message_type):
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

class StatusPanel(QFrame):

    def __init__(self, title, iconPath, parent = None):
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
        self.iconLabel = AlignedLabel(Qt.AlignCenter)
        self.iconLabel.setPixmap(QPixmap(iconPath))
        self.iconLabel.setFixedHeight(60)
        self.titleLabel = AlignedLabel(Qt.AlignCenter, title)
        self.titleLabel.setStyleSheet("font-size: 13px; font-weight: bold;")
        self.lastSyncLabel = InformationLabel("Última sincronización exitosa:\n02:35pm 12-06-2018", InformationLabel.DATE)
        self.message = InformationLabel("", InformationLabel.DISABLE)

        self.layout.addSpacing(5)
        self.layout.addWidget(self.titleLabel)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.iconLabel)
        self.layout.addSpacing(15)
        self.layout.addWidget(self.lastSyncLabel)
        self.layout.addWidget(self.message)
        self.layout.addStretch()

        self.message.setMessage("Todo funciona correctamente", InformationLabel.SUCCESS)