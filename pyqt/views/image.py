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

from utils.paths import get_css_path
from utils.styles import load_css


class ImageView(QWidget):
    # class ImageView():
    def __init__(self, view_instance):
        super(ImageView, self).__init__()
        self.view_instance = view_instance
        self.window = view_instance.window
        # self.window.setWindowTitle("Image Viewer")
        # self.window.setGeometry(100, 100, 800, 600)

        # self.central_widget = QWidget(self.window)
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        # self.image_scroll_area = QScrollArea(self.window)
        # self.image_container = QWidget(self.window)
        self.image_scroll_area = QScrollArea()
        self.image_container = QWidget()
        self.image_layout = QVBoxLayout(self.image_container)

        self.config_button = QPushButton("Open Config Page", self.window)
        self.config_button.clicked.connect(self.open_config_page)

        self.folder_button = QPushButton("Select Folder", self.window)
        self.folder_button.clicked.connect(self.select_folder)

        self.show_folder_checkbox = QCheckBox(
            "Show Images and Videos from Folders", self.window)

        self.progress_bar = QProgressBar(self.window)
        self.progress_bar.setVisible(False)

        self.central_layout.addWidget(self.image_scroll_area)
        self.central_layout.addWidget(self.config_button)
        self.central_layout.addWidget(self.folder_button)
        self.central_layout.addWidget(self.show_folder_checkbox)
        self.central_layout.addWidget(self.progress_bar)

        self.image_container.setLayout(self.image_layout)
        self.image_scroll_area.setWidget(self.image_container)
        self.image_scroll_area.setWidgetResizable(True)

        self.setLayout(self.central_layout)
        # self.central_widget.setLayout(self.central_layout)

        # self.window.setCentralWidget(self.central_widget)

        load_css(self, get_css_path().get("image"))
        # Load external CSS file
        # with open('pyqt/styles/image.css', 'r') as file:
        #     style_sheet = file.read()
        #     # self.window.setStyleSheet(style_sheet)
        #     self.setStyleSheet(style_sheet)

    def open_config_page(self):
        # Add your code to open the configuration page
        print("Opening Config Page")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self.window, "Select Folder")
        if folder_path:
            self.view_instance.presenter.on_folder_selected(
                folder_path)

    def load_folder_contents(self, folder_contents):
        self.clear_icons()

        row_layout = None
        row_count = 0
        for file_info in folder_contents:
            pixmap = QPixmap(file_info["pixmap"])
            file_name = file_info["name"]
            file_path = file_info["path"]

            icon_label = QLabel(self.window)
            icon_label.setPixmap(pixmap.scaledToWidth(50))
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setToolTip(file_name)  # Set the full name as a tooltip

            displayed_name = ((
                file_name[:self.view_instance.presenter.model.image_model.max_name_length] + '...')
                if len(file_name) > self.view_instance.presenter.model.image_model.max_name_length
                else file_name
            )
            name_label = QLabel(displayed_name, self.window)
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setToolTip(file_path)  # Set the full path as a tooltip

            item_layout = QVBoxLayout()
            item_layout.addWidget(icon_label)
            item_layout.addWidget(name_label)

            if row_layout is None:
                row_layout = QHBoxLayout()
                self.image_layout.addLayout(row_layout)
                row_count += 1

            row_layout.addLayout(item_layout)
            print(dir(self.view_instance))
            if row_layout.count() >= self.view_instance.presenter.model.image_model.max_items_per_row:
                row_layout = None

    def clear_icons(self):
        while self.image_layout.count() > 0:
            row_layout = self.image_layout.takeAt(0)
            while row_layout.count() > 0:
                item_layout = row_layout.takeAt(0)
                while item_layout.count() > 0:
                    item = item_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
                        widget.deleteLater()
                    del item
                item_layout.setParent(None)
            row_layout.setParent(None)

    def update_progress_bar(self, current_value):
        # Simulate loading progress
        current_value = int(current_value*100)
        self.progress_bar.setValue(current_value)

        if current_value >= 100:
            self.progress_bar.setVisible(False)
