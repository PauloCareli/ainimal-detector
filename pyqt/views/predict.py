import os
import sys
from PyQt5.QtWidgets import (
    QProgressBar, QTableWidget, QPushButton, QFileDialog, QLineEdit,
    QLabel, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QMessageBox,
    QGroupBox, QGridLayout, QScrollArea, QDialog, QTextEdit, QFrame
)
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QFont


class PredictView(QWidget):
    def __init__(self, view_instance):
        super(PredictView, self).__init__()

        self.view_instance = view_instance
        self.ai_models = []
        self.model = None
        self.output_path = ""

        self.setup_ui()

    def setup_ui(self):
        """Setup the modern predict UI"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("AI Model Prediction")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # Model Selection Group
        model_group = self.create_model_selection_group()
        content_layout.addWidget(model_group)

        # Input Selection Group
        input_group = self.create_input_selection_group()
        content_layout.addWidget(input_group)

        # Progress Section
        progress_group = self.create_progress_group()
        content_layout.addWidget(progress_group)

        # Action Buttons
        self.create_action_buttons()

        # Add stretch to push content to top
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area)

        # Add buttons layout
        self.main_layout.addLayout(self.action_buttons_layout)

        self.update_model_label()

    def create_model_selection_group(self):
        """Create model selection group"""
        group = QGroupBox("AI Model Selection")
        layout = QGridLayout(group)
        layout.setSpacing(15)

        # Model selection dropdown
        model_label = QLabel("Select Model:")
        model_label.setToolTip("Choose an AI model for prediction")
        layout.addWidget(model_label, 0, 0)

        self.model_combo_box = QComboBox()
        self.model_combo_box.addItems(
            [model.name for model in self.ai_models] if self.ai_models else ["No models available"])
        self.model_combo_box.setToolTip(
            "Available AI models for animal detection")
        self.model_combo_box.currentIndexChanged.connect(
            self.update_model_label)
        self.style_dropdown(self.model_combo_box)
        layout.addWidget(self.model_combo_box, 0, 1)

        # Model details button
        self.details_button = QPushButton("View Details")
        self.details_button.setToolTip(
            "View detailed information about the selected model")
        self.details_button.clicked.connect(self.show_model_details)
        self.style_button(self.details_button, "secondary")
        layout.addWidget(self.details_button, 0, 2)

        # Model description
        self.model_description_label = QLabel("Model: No model selected")
        self.model_description_label.setStyleSheet(
            "color: gray; font-size: 12px; padding: 8px;")
        self.model_description_label.setToolTip(
            "Description and details of the currently selected model")
        layout.addWidget(self.model_description_label, 1, 0, 1, 3)

        return group

    def create_input_selection_group(self):
        """Create input selection group"""
        group = QGroupBox("Input Selection")
        layout = QGridLayout(group)
        layout.setSpacing(15)

        # Folder selection
        folder_label = QLabel("Input Folder:")
        folder_label.setToolTip(
            "Select folder containing images/videos to process")
        layout.addWidget(folder_label, 0, 0)

        self.path_line_edit = QLineEdit()
        self.path_line_edit.setPlaceholderText(
            "Click 'Browse' to select a folder with images/videos...")
        self.path_line_edit.setReadOnly(True)
        self.path_line_edit.setToolTip(
            "Path to the folder containing media files for prediction")
        self.style_input_field(self.path_line_edit)
        layout.addWidget(self.path_line_edit, 0, 1)

        # Browse button
        self.select_folder_button = QPushButton("Browse")
        self.select_folder_button.setToolTip(
            "Click to select a folder using file dialog")
        self.select_folder_button.clicked.connect(self.select_folder)
        self.style_button(self.select_folder_button, "secondary")
        layout.addWidget(self.select_folder_button, 0, 2)

        return group

    def create_progress_group(self):
        """Create progress tracking group"""
        group = QGroupBox("Progress")
        layout = QVBoxLayout(group)
        layout.setSpacing(10)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
                padding: 2px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #00ccff;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready to predict")
        self.status_label.setStyleSheet(
            "color: gray; font-size: 12px; padding: 5px;")
        layout.addWidget(self.status_label)

        return group

    def create_action_buttons(self):
        """Create action buttons"""
        self.action_buttons_layout = QHBoxLayout()
        self.action_buttons_layout.addStretch()
        self.action_buttons_layout.setSpacing(15)

        # Predict button
        self.predict_button = QPushButton("Start Prediction")
        self.predict_button.setToolTip(
            "Start AI prediction on the selected folder\nResults will be saved and opened automatically")
        self.predict_button.clicked.connect(self.predict)
        self.style_button(self.predict_button, "primary")
        self.action_buttons_layout.addWidget(self.predict_button)

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
        if not self.ai_models:
            return []
        # Function to find instances with specific attribute value
        matches = [instance for instance in self.ai_models if getattr(
            instance, "name", None) == name]
        return matches[0] if matches else None

    def update_output_path(self):
        folder_path = self.path_line_edit.text()
        self.output_path = folder_path + "/output"

    def show_model_details(self):
        """Show detailed model information in a custom modal dialog"""
        selected_model_name = self.model_combo_box.currentText()

        if not selected_model_name or selected_model_name == "No models available":
            QMessageBox.warning(self, "No Model Selected",
                                "Please select a model to view its details.")
            return

        # Find the selected model
        selected_model = self.find_instance_by_name(selected_model_name)

        if not selected_model:
            QMessageBox.warning(
                self, "Model Not Found", f"Could not find details for model: {selected_model_name}")
            return

        # Create and show the custom modal dialog
        dialog = ModelDetailsDialog(selected_model, self)
        dialog.exec_()

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Directory")
        if folder_path:
            self.path_line_edit.setText(folder_path)
            self.update_output_path()

    def predict(self):
        """Start the prediction process"""
        folder_path = self.path_line_edit.text()
        selected_model = self.model_combo_box.currentText()

        if not folder_path:
            QMessageBox.warning(
                self, "Input Required", "Please select a folder containing images/videos.")
            return

        if not selected_model or selected_model == "No models available":
            QMessageBox.warning(self, "Model Required",
                                "Please select an AI model for prediction.")
            return

        # Start prediction process
        self.status_label.setText("Starting prediction...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.predict_button.setEnabled(False)

        try:
            # Update progress
            self.update_progress_bar(0.1)
            self.status_label.setText("Preparing model...")

            # Ensure output path exists
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

            self.update_progress_bar(0.2)
            self.status_label.setText(
                f"Running prediction with {selected_model}...")

            # Perform the actual prediction
            output_path = self.view_instance.presenter.predict(
                folder_path, self.model)

            self.update_progress_bar(0.9)
            self.status_label.setText("Finalizing results...")

            # Success message
            self.update_progress_bar(1.0)
            self.status_label.setText("Prediction completed successfully!")

            QMessageBox.information(
                self, "Prediction Complete",
                f"Prediction completed using {selected_model}.\n"
                f"Input folder: {folder_path}\n"
                f"Results will open automatically."
            )

            # Open the output folder
            project_root = os.getcwd()
            output_folder_path = os.path.join(project_root, output_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(output_folder_path))

        except Exception as e:
            self.status_label.setText("Prediction failed!")
            QMessageBox.critical(
                self, "Prediction Error",
                f"An error occurred during prediction:\n{str(e)}"
            )
        finally:
            self.predict_button.setEnabled(True)
            # Hide progress bar after a short delay
            self.progress_bar.setVisible(False)

    def update_progress_bar(self, progress_ratio):
        """Update progress bar with a ratio between 0.0 and 1.0"""
        progress_value = int(progress_ratio * 100)
        self.progress_bar.setValue(progress_value)

    def get_current_theme(self):
        """Safely get the current theme"""
        try:
            if hasattr(self.view_instance, 'presenter') and self.view_instance.presenter:
                return getattr(self.view_instance.presenter.model.settings_model, 'theme', 'light')
        except (AttributeError, TypeError):
            pass
        return 'light'

    def style_button(self, button, button_type="primary"):
        """Apply consistent styling to buttons"""
        base_style = """
            QPushButton {
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #333;
                border-radius: 8px;
                min-width: 120px;
                text-align: center;
            }
        """

        if button_type == "primary":
            specific_style = """
                QPushButton {
                    background-color: #00ccff;
                    color: #000;
                }
                QPushButton:hover {
                    background-color: #00a3cc;
                    border-color: #007e9e;
                }
                QPushButton:pressed {
                    background-color: #007e9e;
                }
                QPushButton:disabled {
                    background-color: #ccc;
                    color: #666;
                    border-color: #999;
                }
            """
        else:  # secondary
            specific_style = """
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border-color: #999;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QPushButton:disabled {
                    background-color: #f8f8f8;
                    color: #ccc;
                    border-color: #ddd;
                }
            """

        button.setStyleSheet(base_style + specific_style)

    def style_dropdown(self, dropdown):
        """Apply consistent styling to dropdowns"""
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            border_color = "#555"
            arrow_color = "#CCC"
        else:
            bg_color = "#FFFFFF"
            text_color = "#000000"
            border_color = "#CCC"
            arrow_color = "#666"

        dropdown.setStyleSheet(f"""
            QComboBox {{
                padding: 4px 8px;
                font-size: 12px;
                border: 1px solid {border_color};
                border-radius: 4px;
                min-width: 120px;
                max-width: 200px;
                height: 24px;
                background-color: {bg_color};
                color: {text_color};
            }}
            QComboBox:hover {{
                border-color: #00ccff;
            }}
            QComboBox:focus {{
                border-color: #00ccff;
                outline: none;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 16px;
            }}
            QComboBox::down-arrow {{
                image: none;
                width: 0px;
                height: 0px;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {arrow_color};
                margin-right: 5px;
                margin-top: 2px;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid #00ccff;
                background-color: {bg_color};
                color: {text_color};
                selection-background-color: #00ccff;
                selection-color: white;
            }}
        """)

    def style_input_field(self, field):
        """Apply consistent styling to input fields"""
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            border_color = "#555"
        else:
            bg_color = "#FFFFFF"
            text_color = "#000000"
            border_color = "#CCC"

        field.setStyleSheet(f"""
            QLineEdit {{
                padding: 4px 8px;
                font-size: 12px;
                border: 1px solid {border_color};
                border-radius: 4px;
                height: 24px;
                background-color: {bg_color};
                color: {text_color};
            }}
            QLineEdit:hover {{
                border-color: #00ccff;
            }}
            QLineEdit:focus {{
                border-color: #00ccff;
                outline: none;
            }}
            QLineEdit:read-only {{
                background-color: {bg_color};
                color: {text_color};
            }}
        """)

    def refresh_styling(self):
        """Refresh all component styling - useful when theme changes"""
        try:
            self.style_dropdown(self.model_combo_box)
            self.style_input_field(self.path_line_edit)
            self.style_button(self.details_button, "secondary")
            self.style_button(self.select_folder_button, "secondary")
            self.style_button(self.predict_button, "primary")
        except AttributeError:
            # Some components might not be created yet
            pass


class ModelDetailsDialog(QDialog):
    """Custom modal dialog for displaying detailed model information"""

    def __init__(self, model, parent=None):
        super(ModelDetailsDialog, self).__init__(parent)
        self.model = model
        self.parent_view = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup the modal dialog UI"""
        self.setWindowTitle(f"Model Details - {self.model.name}")
        self.setModal(True)
        self.setMinimumSize(700, 800)
        self.resize(700, 800)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel(f"{self.model.name}")
        title_font = QFont()
        title_font.setPointSize(26)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "color: #00ccff; padding: 15px; margin-bottom: 15px; font-size: 26px;")
        main_layout.addWidget(title_label)

        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(15, 15, 15, 15)

        # Model information sections
        self.create_model_info_sections(content_layout)

        # Add stretch to push content to top
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Close button
        self.create_close_button(main_layout)

        # Apply styling
        self.apply_styling()

    def create_model_info_sections(self, layout):
        """Create information sections for the model"""

        # Basic Information
        basic_group = QGroupBox("Basic Information")
        basic_group.setStyleSheet(
            "QGroupBox { font-size: 14px; font-weight: bold; }")
        basic_layout = QGridLayout(basic_group)
        basic_layout.setSpacing(12)

        # Model name
        name_label_title = QLabel("Name:")
        name_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        basic_layout.addWidget(name_label_title, 0, 0)
        name_label = QLabel(getattr(self.model, 'name', 'Unknown'))
        name_label.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #00ccff; padding: 5px;")
        basic_layout.addWidget(name_label, 0, 1)

        # Model type
        type_label_title = QLabel("Type:")
        type_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        basic_layout.addWidget(type_label_title, 1, 0)
        model_type = getattr(self.model, 'model_type', 'YOLO v8')
        type_label = QLabel(model_type)
        type_label.setStyleSheet("font-size: 12px; padding: 5px;")
        basic_layout.addWidget(type_label, 1, 1)

        # Version
        version_label_title = QLabel("Version:")
        version_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        basic_layout.addWidget(version_label_title, 2, 0)
        version = getattr(self.model, 'version', '1.0.0')
        version_label = QLabel(version)
        version_label.setStyleSheet("font-size: 12px; padding: 5px;")
        basic_layout.addWidget(version_label, 2, 1)

        # Training date
        date_label_title = QLabel("Training Date:")
        date_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        basic_layout.addWidget(date_label_title, 3, 0)
        training_date = getattr(self.model, 'training_date', 'Not specified')
        date_label = QLabel(training_date)
        date_label.setStyleSheet("font-size: 12px; padding: 5px;")
        basic_layout.addWidget(date_label, 3, 1)

        layout.addWidget(basic_group)

        # Performance Metrics
        performance_group = QGroupBox("Performance Metrics")
        performance_group.setStyleSheet(
            "QGroupBox { font-size: 14px; font-weight: bold; }")
        perf_layout = QGridLayout(performance_group)
        perf_layout.setSpacing(12)

        # Accuracy
        acc_label_title = QLabel("Accuracy:")
        acc_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        perf_layout.addWidget(acc_label_title, 0, 0)
        accuracy = getattr(self.model, 'accuracy', 0.0)
        accuracy_label = QLabel(f"{accuracy:.1%}")
        accuracy_color = "#28a745" if accuracy > 0.8 else "#ffc107"
        accuracy_label.setStyleSheet(
            f"font-size: 12px; font-weight: bold; color: {accuracy_color}; padding: 5px;")
        perf_layout.addWidget(accuracy_label, 0, 1)

        # Default threshold
        thresh_label_title = QLabel("Default Threshold:")
        thresh_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        perf_layout.addWidget(thresh_label_title, 1, 0)
        threshold = getattr(self.model, 'threshold', 0.0)
        thresh_label = QLabel(f"{threshold:.2f}")
        thresh_label.setStyleSheet("font-size: 12px; padding: 5px;")
        perf_layout.addWidget(thresh_label, 1, 1)

        # mAP (mean Average Precision)
        map_label_title = QLabel("mAP@0.5:")
        map_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        perf_layout.addWidget(map_label_title, 2, 0)
        map_score = getattr(self.model, 'map_50', 'Not available')
        map_label = QLabel(str(map_score))
        map_label.setStyleSheet("font-size: 12px; padding: 5px;")
        perf_layout.addWidget(map_label, 2, 1)

        # Training dataset size
        images_label_title = QLabel("Training Images:")
        images_label_title.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 5px;")
        perf_layout.addWidget(images_label_title, 3, 0)
        training_images = getattr(
            self.model, 'training_images', 'Not specified')
        images_label = QLabel(str(training_images))
        images_label.setStyleSheet("font-size: 12px; padding: 5px;")
        perf_layout.addWidget(images_label, 3, 1)

        layout.addWidget(performance_group)

        # Capabilities
        capabilities_group = QGroupBox("Model Capabilities")
        cap_layout = QVBoxLayout(capabilities_group)

        # Supported classes
        classes_label = QLabel("Detectable Classes:")
        classes_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        cap_layout.addWidget(classes_label)

        classes = getattr(self.model, 'classes', ['Dog', 'Cat', 'Wild Animal'])
        classes_text = ", ".join(classes)
        classes_display = QLabel(classes_text)
        classes_display.setWordWrap(True)
        classes_display.setStyleSheet(
            "padding: 8px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px;")
        cap_layout.addWidget(classes_display)

        # Input requirements
        input_label = QLabel("Input Requirements:")
        input_label.setStyleSheet(
            "font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        cap_layout.addWidget(input_label)

        input_size = getattr(self.model, 'input_size', '640x640')
        input_formats = getattr(self.model, 'supported_formats', [
                                'jpg', 'png', 'mp4', 'avi'])
        input_text = f"Image Size: {input_size}\nSupported Formats: {', '.join(input_formats)}"
        input_display = QLabel(input_text)
        input_display.setStyleSheet(
            "padding: 8px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px;")
        cap_layout.addWidget(input_display)

        layout.addWidget(capabilities_group)

        # Description
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout(desc_group)

        description = getattr(self.model, 'description',
                              'No description available')
        desc_text = QTextEdit()
        desc_text.setPlainText(description)
        desc_text.setReadOnly(True)
        desc_text.setMaximumHeight(80)
        desc_text.setStyleSheet(
            "border: 1px solid #dee2e6; border-radius: 4px; padding: 8px;")
        desc_layout.addWidget(desc_text)

        layout.addWidget(desc_group)

        # File Information
        file_group = QGroupBox("File Information")
        file_layout = QGridLayout(file_group)
        file_layout.setSpacing(10)

        # File path
        file_layout.addWidget(QLabel("Path:"), 0, 0)
        path = getattr(self.model, 'path', 'Unknown')
        path_label = QLabel(path)
        path_label.setWordWrap(True)
        path_label.setStyleSheet("font-family: monospace; font-size: 10px;")
        file_layout.addWidget(path_label, 0, 1)

        # File size
        file_layout.addWidget(QLabel("Size:"), 1, 0)
        file_size = self.get_file_size(path)
        file_layout.addWidget(QLabel(file_size), 1, 1)

        layout.addWidget(file_group)

    def create_close_button(self, layout):
        """Create the close button"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def get_file_size(self, file_path):
        """Get the size of the model file"""
        try:
            if os.path.exists(file_path):
                size_bytes = os.path.getsize(file_path)
                if size_bytes < 1024:
                    return f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    return f"{size_bytes / 1024:.1f} KB"
                elif size_bytes < 1024 * 1024 * 1024:
                    return f"{size_bytes / (1024 * 1024):.1f} MB"
                else:
                    return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
            else:
                return "File not found"
        except Exception:
            return "Unknown"

    def apply_styling(self):
        """Apply consistent styling to the dialog"""
        # Get current theme
        current_theme = 'light'  # Default fallback
        try:
            if hasattr(self.parent_view, 'get_current_theme'):
                current_theme = self.parent_view.get_current_theme()
        except:
            pass

        if current_theme == 'dark':
            self.setStyleSheet("""
                QDialog {
                    background-color: #2E2E2E;
                    color: #FFFFFF;
                    font-size: 12px;
                }
                QGroupBox {
                    font-size: 14px;
                    font-weight: bold;
                    border: 2px solid #555;
                    border-radius: 5px;
                    margin-top: 15px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #00ccff;
                    font-size: 14px;
                    font-weight: bold;
                }
                QLabel {
                    color: #FFFFFF;
                    font-size: 12px;
                }
                QTextEdit {
                    background-color: #3E3E3E;
                    color: #FFFFFF;
                    border: 1px solid #555;
                    font-size: 12px;
                }
                QScrollArea {
                    border: none;
                    background-color: #2E2E2E;
                }
            """)
        else:
            self.setStyleSheet("""
                QDialog {
                    background-color: #FFFFFF;
                    color: #000000;
                    font-size: 12px;
                }
                QGroupBox {
                    font-size: 14px;
                    font-weight: bold;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    margin-top: 15px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: #00ccff;
                    font-size: 14px;
                    font-weight: bold;
                }
                QLabel {
                    color: #000000;
                    font-size: 12px;
                }
                QTextEdit {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #ddd;
                    font-size: 12px;
                }
                QScrollArea {
                    border: none;
                    background-color: #FFFFFF;
                }
            """)
