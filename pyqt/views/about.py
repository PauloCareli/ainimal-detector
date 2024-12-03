from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AboutView(QWidget):
    def __init__(self, view_instance):
        super(AboutView, self).__init__()

        self.view_instance = view_instance

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)  # Center-align the content

        # Title
        title_label = QLabel("AInimal Detector 1.0")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # Add about information
        about_label = QLabel(
            "<html>"
            "<p><b>Author:</b> Paulo Careli</p>"
            "<p><b>Reach me out on:</b> <a href='https://www.linkedin.com/in/paulo-careli/'>LinkedIn</a></p>"
            "<p><b>Learn more about the project:</b> <a href='https://github.com/PauloCareli/camera-trap-animal-detection-with-deep-learning'>here</a></p>"
            "<p><b>Contact me at:</b> <a href='mailto:paulohcareli@gmail.com'>paulohcareli@gmail.com</a></p>"
            "</html>"
        )

        about_label.setOpenExternalLinks(True)
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setStyleSheet(
            "font-size: 16px")

        self.layout.addWidget(about_label)

        # Add stretch to fill remaining space
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.setStyleSheet("QWidget { padding: 20px; }")
