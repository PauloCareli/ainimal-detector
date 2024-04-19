import os
import sys
from PyQt5.QtWidgets import QProgressBar, QTableWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices


class PredictView(QWidget):
    def __init__(self, view_instance):
        super(PredictView, self).__init__()

        self.view_instance = view_instance

        # Create a table widget and a layout for the central widget
        # self.central_widget = QTableWidget(self)
        self.central_layout = QVBoxLayout()
        # self.central_layout.addWidget(self.central_widget)

        # self.about_label = QLabel(
        #     "<html><p>AInimal detector 1.0</p>"
        #     "<p>Author: Paulo Careli</p>"
        #     "<p>Reach me out on <a href='https://www.linkedin.com/in/paulo-careli/'>LinkedIn</a>.</p>"
        #     "<p>Learn more about the project <a href='https://github.com/PauloCareli/camera-trap-animal-detection-with-deep-learning'>here</a>.</p>"
        #     "<p>Contact me at: <a href='mailto:paulo.careli@engenharia.ufjf.br'>paulo.careli@engenharia.ufjf.br</a></p></html>"
        # )
        # self.about_label.setOpenExternalLinks(True)
        # self.layout = QVBoxLayout(self)
        # self.layout.addWidget(self.about_label)
        # self.layout.addStretch()  # Add stretch to fill remaining space
        self.ai_models = []
        self.model = None

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 600, 200)
        self.setWindowTitle('AI Model Prediction App')
        button_height = 40

        self.ai_model_layout = QVBoxLayout()
        self.ai_model_layout_row = QHBoxLayout()
        # Dropdown for selecting AI Model
        self.select_model_label = QLabel(
            "Select a Model:"
        )
        self.select_model_label.setGeometry(220, 50, 250, button_height)

        # Dropdown
        self.model_combo_box = QComboBox(self)
        self.model_combo_box.setGeometry(50, 50, 150, button_height)
        # Add your model names here
        self.model_combo_box.addItems(
            [model.name for model in self.ai_models] if self.ai_models else [])
        self.model_combo_box.currentIndexChanged.connect(
            self.update_model_label)

        # Label to display selected model name
        self.model_name_label = QLabel(self)
        self.model_name_label.setGeometry(220, 50, 150, button_height)

        # Details button
        self.details_button = QPushButton('Details', self)
        self.details_button.setGeometry(400, 50, 100, button_height)
        self.details_button.clicked.connect(self.show_model_details)

        self.model_description_label = QLabel("Model selected: <p></p>", self)
        self.model_description_label.setGeometry(220, 50, 250, button_height)

        # Add to model line
        self.ai_model_layout_row.addWidget(self.model_combo_box)
        self.ai_model_layout_row.addWidget(self.model_name_label)
        self.ai_model_layout_row.addWidget(self.details_button)
        self.ai_model_layout.addWidget(self.select_model_label)
        self.ai_model_layout.addLayout(self.ai_model_layout_row)
        self.ai_model_layout.addWidget(self.model_description_label)

        self.select_folder_layout = QHBoxLayout()
        # Select Folder button
        self.select_folder_button = QPushButton('Select Folder', self)
        self.select_folder_button.setGeometry(50, 100, 150, button_height)
        self.select_folder_button.clicked.connect(self.select_folder)

        # Path Line Edit widget
        self.path_line_edit = QLineEdit(self)
        self.path_line_edit.setGeometry(220, 100, 250, button_height)
        self.path_line_edit.setPlaceholderText('Selected Folder Path')

        self.select_folder_layout.addWidget(self.select_folder_button)
        self.select_folder_layout.addWidget(self.path_line_edit)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.predict_button_layout = QHBoxLayout()
        # Predict button
        self.predict_button = QPushButton('Predict', self)
        # self.predict_button.setGeometry(400, 100, 100, button_height)
        self.predict_button.setFixedHeight(40)
        self.predict_button.clicked.connect(self.predict)
        self.predict_button_layout.addWidget(self.predict_button)

        # Add buttons to the layout
        self.central_layout.addLayout(self.ai_model_layout)
        self.central_layout.addLayout(self.select_folder_layout)
        self.central_layout.addWidget(self.progress_bar)
        self.central_layout.addLayout(self.predict_button_layout)

        self.central_layout.setStretch(0, 20)
        self.central_layout.setStretch(1, 20)
        self.central_layout.setStretch(2, 10)
        self.setLayout(self.central_layout)

        self.update_model_label()

    def update_model_label(self):
        selected_model = self.model_combo_box.currentText()
        self.model_description_label.setText(
            f"Model selected: {selected_model}")
        self.set_current_model(selected_model)

    def update_models(self):
        self.model_combo_box.clear()
        self.model_combo_box.addItems(
            [model.name for model in self.ai_models] if self.ai_models else [])

    def set_current_model(self, name):
        self.model = self.find_instance_by_name(name)

    def find_instance_by_name(self, name):
        # Function to find instances with specific attribute value
        return [instance for instance in self.ai_models if getattr(instance, "name") == name]

    def update_output_path(self):
        folder_path = self.path_line_edit.text()
        self.output_path = folder_path + "/output"

    def show_model_details(self):
        selected_model = self.model_name_label.text()
        details_message = f"Details for {selected_model}:\n\nDescription: ...\nParameters: ..."
        QMessageBox.information(self, "Model Details", details_message)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Directory")
        if folder_path:
            self.path_line_edit.setText(folder_path)
            self.update_output_path()

    def predict(self):
        self.progress_bar.setVisible(True)
        self.update_progress_bar(10)

        folder_path = self.path_line_edit.text()
        selected_model = self.model_combo_box.currentText()

        if folder_path and selected_model and self.output_path:
            # Ensure output path exists or create it if not
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

            self.view_instance.presenter.predict(folder_path, self.model)
            # Perform prediction using folder_path and selected_model
            # Replace this with your actual prediction function
            QMessageBox.information(
                self, "Prediction", f"Predicting using {selected_model} on folder: {folder_path}")

            # Open the output path using the system's default file manager
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_path))

        else:
            QMessageBox.warning(
                self, "Error", "Please select a folder and an AI model.")

    def update_progress_bar(self, current_value):
        # Simulate loading progress
        current_value = int(current_value*100)
        self.progress_bar.setValue(current_value)

        if current_value >= 100:
            self.progress_bar.setVisible(False)
