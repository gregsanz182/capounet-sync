from PyQt5.QtWidgets import QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

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