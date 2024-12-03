from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QCheckBox,
    QScrollArea,
    QWidget,
    QProgressBar
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ConfigView(QWidget):
    # class ConfigView():
    def __init__(self, view_instance):
        super(ConfigView, self).__init__()

        self.view_instance = view_instance

        self.label = QLabel("Settings Page. Coming soon...")
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addStretch()  # Add stretch to fill remaining space
