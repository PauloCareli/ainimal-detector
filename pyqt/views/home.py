from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt

from utils.paths import get_image_path


class HomeView(QWidget):
    def __init__(self, view_instance):
        super(HomeView, self).__init__()

        self.view_instance = view_instance

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Header
        text_label = QLabel("Welcome to AInimal Detector!", self)

        text_label.setFont(QFont("Arial", 28, QFont.Bold))
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

        # Add image
        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignCenter)

        # Load the image
        image_path = get_image_path().get("welcome")

        image = QImage(image_path)

        if image.isNull():
            image_label.setText("Image could not be loaded.")
            image_label.setStyleSheet("color: red; font-size: 16px;")
        else:
            pixmap = QPixmap.fromImage(image)
            image_label.setPixmap(pixmap)

        layout.addWidget(image_label)

        # Set the layout for the HomeView
        self.setLayout(layout)
