from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QCheckBox,
    QScrollArea,
    QWidget,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QGroupBox,
    QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


class ConfigView(QWidget):
    # Signal to notify when settings are saved
    settings_saved = pyqtSignal(dict)

    def __init__(self, view_instance):
        super(ConfigView, self).__init__()

        self.view_instance = view_instance
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Setup the settings UI"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("Settings")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Scroll area for settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)

        # General Settings Group
        general_group = self.create_general_settings_group()
        content_layout.addWidget(general_group)

        # AI Model Settings Group
        ai_model_group = self.create_ai_model_settings_group()
        content_layout.addWidget(ai_model_group)

        # Output Settings Group
        output_group = self.create_output_settings_group()
        content_layout.addWidget(output_group)

        # Add stretch to push content to top
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        self.main_layout.addWidget(scroll_area)

        # Buttons
        self.create_buttons()

    def create_general_settings_group(self):
        """Create general settings group"""
        group = QGroupBox("General Settings")
        layout = QGridLayout(group)
        layout.setSpacing(10)

        # Theme selection with mapping
        self.theme_mapping = {
            "Light": "light",
            "Dark": "dark"
        }
        self.reverse_theme_mapping = {
            v: k for k, v in self.theme_mapping.items()}

        theme_label = QLabel("Theme:")
        theme_label.setToolTip(
            "Choose between Light and Dark theme for the application")
        layout.addWidget(theme_label, 0, 0)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(self.theme_mapping.keys()))
        self.theme_combo.setToolTip(
            "Select Light or Dark theme\nChanges apply immediately when saved")
        self.style_dropdown(self.theme_combo)
        layout.addWidget(self.theme_combo, 0, 1)

        return group

    def create_ai_model_settings_group(self):
        """Create AI model settings group"""
        group = QGroupBox("AI Model Settings")
        layout = QGridLayout(group)
        layout.setSpacing(10)

        # Detection threshold
        threshold_label = QLabel("Detection Threshold:")
        threshold_label.setToolTip(
            "Minimum confidence score for AI detections (0.1 = 10%, 1.0 = 100%)")
        layout.addWidget(threshold_label, 0, 0)

        self.threshold_spin = QDoubleSpinBox()
        self.threshold_spin.setRange(0.1, 1.0)
        self.threshold_spin.setSingleStep(0.05)
        self.threshold_spin.setDecimals(2)
        self.threshold_spin.setValue(0.7)
        self.threshold_spin.setToolTip(
            "Higher values = more confident detections\nLower values = more detections (including false positives)")
        self.style_spinbox(self.threshold_spin)
        layout.addWidget(self.threshold_spin, 0, 1)

        # Threshold description
        threshold_desc = QLabel(
            "Minimum confidence score for detections (0.1 - 1.0)")
        threshold_desc.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(threshold_desc, 1, 0, 1, 2)

        return group

    def create_output_settings_group(self):
        """Create output settings group"""
        group = QGroupBox("Output Settings")
        layout = QGridLayout(group)
        layout.setSpacing(10)

        # Media output path
        media_label = QLabel("Media Output Path:")
        media_label.setToolTip(
            "Directory where processed images and videos will be saved")
        layout.addWidget(media_label, 0, 0)

        self.media_output_edit = QLineEdit()
        self.media_output_edit.setPlaceholderText(
            "Select output directory for processed media...")
        self.media_output_edit.setToolTip(
            "Full path to the directory for saving processed media files")
        self.style_input_field(self.media_output_edit)
        layout.addWidget(self.media_output_edit, 0, 1)

        self.media_browse_btn = QPushButton("Browse")
        self.media_browse_btn.setToolTip(
            "Click to select a folder using file dialog")
        self.media_browse_btn.clicked.connect(self.browse_media_output)
        self.style_button(self.media_browse_btn, "secondary")
        layout.addWidget(self.media_browse_btn, 0, 2)

        # Report output path
        report_label = QLabel("Report Output Path:")
        report_label.setToolTip(
            "Directory where detection reports and analysis files will be saved")
        layout.addWidget(report_label, 1, 0)

        self.report_output_edit = QLineEdit()
        self.report_output_edit.setPlaceholderText(
            "Select output directory for reports...")
        self.report_output_edit.setToolTip(
            "Full path to the directory for saving analysis reports")
        self.style_input_field(self.report_output_edit)
        layout.addWidget(self.report_output_edit, 1, 1)

        self.report_browse_btn = QPushButton("Browse")
        self.report_browse_btn.setToolTip(
            "Click to select a folder using file dialog")
        self.report_browse_btn.clicked.connect(self.browse_report_output)
        self.style_button(self.report_browse_btn, "secondary")
        layout.addWidget(self.report_browse_btn, 1, 2)

        # Recursive folder search
        self.recursive_checkbox = QCheckBox("Recursive folder search")
        self.recursive_checkbox.setToolTip(
            "When enabled, search through all subdirectories\nWhen disabled, only process files in the selected folder")
        self.style_checkbox(self.recursive_checkbox)
        layout.addWidget(self.recursive_checkbox, 2, 0, 1, 3)

        return group

    def create_buttons(self):
        """Create action buttons"""
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.setSpacing(15)

        # Reset to defaults button
        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.setToolTip(
            "Reset all settings to their default values\nThis will not save automatically")
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        self.style_button(self.reset_btn, "secondary")
        button_layout.addWidget(self.reset_btn)

        # Save button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setToolTip(
            "Save all current settings to file\nTheme changes will apply immediately")
        self.save_btn.clicked.connect(self.save_settings)
        self.style_button(self.save_btn, "primary")
        button_layout.addWidget(self.save_btn)

        self.main_layout.addLayout(button_layout)

    def connect_signals(self):
        """Connect signals to slots"""
        # Additional signal connections can be added here
        self.theme_combo.currentTextChanged.connect(self.on_settings_changed)
        self.recursive_checkbox.stateChanged.connect(self.on_settings_changed)
        self.threshold_spin.valueChanged.connect(self.on_settings_changed)

    def get_current_theme(self):
        """Safely get the current theme"""
        try:
            if hasattr(self.view_instance, 'presenter') and self.view_instance.presenter:
                return getattr(self.view_instance.presenter.model.settings_model, 'theme', 'light')
        except (AttributeError, TypeError):
            pass
        # Default to light theme if presenter isn't available yet
        return 'light'

    def on_settings_changed(self):
        """Called when any setting is changed"""
        # You can add validation or other logic here if needed
        pass

    def browse_media_output(self):
        """Browse for media output directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Media Output Directory", self.media_output_edit.text()
        )
        if directory:
            self.media_output_edit.setText(directory)

    def browse_report_output(self):
        """Browse for report output directory"""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Report Output Directory", self.report_output_edit.text()
        )
        if directory:
            self.report_output_edit.setText(directory)

    def load_settings(self, settings):
        """Load settings into the UI"""
        # Convert internal theme value to display name
        theme_value = settings.get("theme", "light")
        display_name = self.reverse_theme_mapping.get(theme_value, "Light")
        self.theme_combo.setCurrentText(display_name)

        self.media_output_edit.setText(
            settings.get("media_output_path", "pyqt/output"))
        self.report_output_edit.setText(
            settings.get("report_output_path", settings.get("report", "pyqt/reports")))  # Backward compatibility
        self.recursive_checkbox.setChecked(
            settings.get("recursive_folder_search", False))
        self.threshold_spin.setValue(settings.get("threshold", 0.7))

    def get_settings(self):
        """Get current settings from UI"""
        # Convert display name back to internal theme value
        display_name = self.theme_combo.currentText()
        theme_value = self.theme_mapping.get(display_name, "light")

        return {
            "theme": theme_value,
            "media_output_path": self.media_output_edit.text(),
            "report_output_path": self.report_output_edit.text(),
            "recursive_folder_search": self.recursive_checkbox.isChecked(),
            "threshold": self.threshold_spin.value()
        }

    def save_settings(self):
        """Save current settings"""
        settings = self.get_settings()
        self.settings_saved.emit(settings)

    def reset_to_defaults(self):
        """Reset all settings to default values"""
        default_settings = {
            "theme": "light",
            "media_output_path": "pyqt/output",
            "report": "pyqt/reports",
            "recursive_folder_search": False,
            "threshold": 0.7
        }
        self.load_settings(default_settings)

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
                    background-color: #00ccff;
                    border-color: #00ccff;
                }
                QPushButton:pressed {
                    background-color: #007e9e;
                }
            """
        else:  # secondary
            specific_style = """
                QPushButton {
                    background-color: #f0f0f0;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #00ccff;
                    color: white;
                    border-color: #00ccff;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """

        button.setStyleSheet(base_style + specific_style)

    def style_dropdown(self, dropdown):
        """Apply consistent styling to dropdowns"""
        # Get current theme colors
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
                min-width: 100px;
                max-width: 120px;
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
        # Get current theme colors
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
        """)

    def style_spinbox(self, spinbox):
        """Apply consistent styling to spin boxes"""
        # Get current theme colors
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            border_color = "#555"
        else:
            bg_color = "#FFFFFF"
            text_color = "#000000"
            border_color = "#CCC"

        spinbox.setStyleSheet(f"""
            QDoubleSpinBox {{
                padding: 4px 8px;
                font-size: 12px;
                border: 1px solid {border_color};
                border-radius: 4px;
                min-width: 80px;
                max-width: 100px;
                height: 24px;
                background-color: {bg_color};
                color: {text_color};
            }}
            QDoubleSpinBox:hover {{
                border-color: #00ccff;
            }}
            QDoubleSpinBox:focus {{
                border-color: #00ccff;
                outline: none;
            }}
        """)

    def style_checkbox(self, checkbox):
        """Apply consistent styling to checkboxes"""
        # Get current theme colors
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            text_color = "#FFFFFF"
            border_color = "#555"
            bg_color = "#2E2E2E"
        else:
            text_color = "#000000"
            border_color = "#CCC"
            bg_color = "#FFFFFF"

        checkbox.setStyleSheet(f"""
            QCheckBox {{
                font-size: 12px;
                spacing: 6px;
                color: {text_color};
                background-color: transparent;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border: 1px solid {border_color};
                border-radius: 3px;
                background-color: {bg_color};
            }}
            QCheckBox::indicator:hover {{
                border-color: #00ccff;
            }}
            QCheckBox::indicator:checked {{
                background-color: #00ccff;
                border-color: #00ccff;
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: #00a3cc;
            }}
            QCheckBox:disabled {{
                color: #999;
            }}
        """)

    def refresh_styling(self):
        """Refresh all component styling - useful when theme changes"""
        try:
            self.style_dropdown(self.theme_combo)
            self.style_spinbox(self.threshold_spin)
            self.style_input_field(self.media_output_edit)
            self.style_input_field(self.report_output_edit)
            self.style_checkbox(self.recursive_checkbox)
            self.style_button(self.media_browse_btn, "secondary")
            self.style_button(self.report_browse_btn, "secondary")
            self.style_button(self.reset_btn, "secondary")
            self.style_button(self.save_btn, "primary")
        except AttributeError:
            # Some components might not be created yet
            pass
