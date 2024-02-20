from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
)


class AboutView(QWidget):
    def __init__(self, view_instance):
        super(AboutView, self).__init__()

        self.view_instance = view_instance

        self.about_label = QLabel(
            "<html><p>AInimal detector 1.0</p>"
            "<p>Author: Paulo Careli</p>"
            "<p>Reach me out on <a href='https://www.linkedin.com/in/paulo-careli/'>LinkedIn</a>.</p>"
            "<p>Learn more about the project <a href='https://github.com/PauloCareli/camera-trap-animal-detection-with-deep-learning'>here</a>.</p>"
            "<p>Contact me at: <a href='mailto:paulo.careli@engenharia.ufjf.br'>paulo.careli@engenharia.ufjf.br</a></p></html>"
        )
        self.about_label.setOpenExternalLinks(True)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.about_label)
        self.layout.addStretch()  # Add stretch to fill remaining space
