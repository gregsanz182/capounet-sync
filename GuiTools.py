from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QToolButton
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
            return QPixmap("success_icon.png")
        elif message_type == self.ERROR:
            return QPixmap("error_icon.png")
        elif message_type == self.WARNING:
            return QPixmap("warning_icon.png")
        elif message_type == self.DATE:
            return QPixmap("date_icon.png")
        elif message_type == self.DISABLE:
            return QPixmap()

class ToolButton(QToolButton):

    def __init__(self, text="", icon=QIcon(), parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)