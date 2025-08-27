import glob
import os
from datetime import datetime

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QDialog, QFileDialog, QFrame, QGroupBox,
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)


class CSVDataModal(QDialog):
    """Modal dialog to display CSV data in a table"""

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.current_csv_data = None
        self.parent_widget = parent
        self.setup_ui()
        self.apply_theme_styling()
        self.load_csv_data()

    def setup_ui(self):
        """Setup the modal UI"""
        self.setWindowTitle(f"CSV Viewer - {os.path.basename(self.file_path)}")
        self.setModal(True)
        self.resize(1000, 600)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        # Header with file info
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.NoFrame)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)

        # Title
        title_label = QLabel(f"📄 {os.path.basename(self.file_path)}")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        # File info (will be updated with CSV stats later)
        try:
            file_size = os.path.getsize(self.file_path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(self.file_path))
            size_mb = file_size / (1024 * 1024)

            self.info_label = QLabel(
                f"Path: {self.file_path}\nSize: {size_mb:.2f} MB | Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.info_label.setStyleSheet("color: #666; font-size: 11px;")
            self.info_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(self.info_label)
        except Exception:
            self.info_label = QLabel("File information unavailable")
            self.info_label.setStyleSheet("color: #666; font-size: 11px;")
            self.info_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(self.info_label)

        layout.addWidget(header_frame)

        # Status label for loading/error messages
        self.status_label = QLabel("Loading CSV data...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "color: #666; font-size: 14px;")
        layout.addWidget(self.status_label)

        # Table widget for CSV data
        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.setSortingEnabled(True)
        self.data_table.setVisible(False)
        layout.addWidget(self.data_table)

        # Buttons
        button_layout = QHBoxLayout()

        # Export button
        self.export_btn = QPushButton("Export Data")
        self.export_btn.clicked.connect(self.export_data)
        self.export_btn.setEnabled(False)
        self.export_btn.setToolTip("Export the CSV data to a new file")
        button_layout.addWidget(self.export_btn)

        button_layout.addStretch()

        # Data stats label (alternative location for stats)
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet(
            "color: #666; font-size: 11px; margin-right: 15px;")
        # Hidden by default, can be shown as alternative
        self.stats_label.setVisible(False)
        button_layout.addWidget(self.stats_label)

        # Close button
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setDefault(True)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

    def get_current_theme(self):
        """Get current theme from parent widget"""
        try:
            if self.parent_widget and hasattr(self.parent_widget, 'view_instance'):
                view_instance = self.parent_widget.view_instance
                if hasattr(view_instance, 'presenter') and view_instance.presenter:
                    return getattr(view_instance.presenter.model.settings_model, 'theme', 'light')
        except (AttributeError, TypeError):
            pass
        return 'light'

    def apply_theme_styling(self):
        """Apply theme-aware styling to the modal"""
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            # Dark theme colors
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            secondary_bg = "#3E3E3E"
            border_color = "#555555"
            header_bg = "#404040"
            table_bg = "#353535"
            table_alt_bg = "#3A3A3A"
        else:
            # Light theme colors with gray tones instead of white
            bg_color = "#F5F5F5"
            text_color = "#000000"
            secondary_bg = "#E8E8E8"
            border_color = "#CCCCCC"
            header_bg = "#EEEEEE"
            table_bg = "#FAFAFA"
            table_alt_bg = "#F0F0F0"

        # Apply main dialog styling
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
                color: {text_color};
                font-size: 12px;
            }}
            
            QFrame {{
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            
            QLabel {{
                color: {text_color};
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            
            QTableWidget {{
                background-color: {table_bg};
                alternate-background-color: {table_alt_bg};
                color: {text_color};
                border: none;
                gridline-color: {border_color};
            }}
            
            QTableWidget::item {{
                padding: 2px;
                border: none;
                margin: 0px;
            }}
            
            QTableWidget::item:selected {{
                background-color: #00ccff;
                color: white;
            }}
            
            QHeaderView::section {{
                background-color: {secondary_bg};
                color: {text_color};
                padding: 2px 4px;
                border: none;
                font-weight: bold;
                margin: 0px;
            }}
            
            QHeaderView::down-arrow {{
                color: {text_color};
                width: 12px;
                height: 12px;
            }}
            
            QHeaderView::up-arrow {{
                color: {text_color};
                width: 12px;
                height: 12px;
            }}
            
            QPushButton {{
                background-color: {secondary_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 3px;
                padding: 4px 8px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: #00ccff;
                color: white;
                border-color: #00ccff;
            }}
            
            QPushButton:pressed {{
                background-color: #3A80D2;
                color: white;
            }}
        """)

    def load_csv_data(self):
        """Load CSV data into the table"""
        try:
            self.status_label.setText("Loading CSV data...")

            # Read CSV data
            df = pd.read_csv(self.file_path)
            self.current_csv_data = df

            # Set up table
            self.data_table.setRowCount(df.shape[0])
            self.data_table.setColumnCount(df.shape[1])
            self.data_table.setHorizontalHeaderLabels(df.columns.tolist())

            # Populate table
            for row in range(df.shape[0]):
                for col in range(df.shape[1]):
                    value = df.iat[row, col]
                    # Handle NaN values
                    if pd.isna(value):
                        value = ""
                    item = QTableWidgetItem(str(value))
                    self.data_table.setItem(row, col, item)

            # Resize columns to content (but limit width)
            self.data_table.resizeColumnsToContents()
            for col in range(df.shape[1]):
                width = self.data_table.columnWidth(col)
                if width > 200:  # Limit column width
                    self.data_table.setColumnWidth(col, 200)

            # Show table and hide status label
            self.data_table.setVisible(True)
            self.status_label.setVisible(False)
            self.export_btn.setEnabled(True)

            # Update header with CSV statistics
            try:
                file_size = os.path.getsize(self.file_path)
                mod_time = datetime.fromtimestamp(
                    os.path.getmtime(self.file_path))
                size_mb = file_size / (1024 * 1024)

                # Add CSV stats to the header info
                self.info_label.setText(
                    f"Path: {self.file_path}\n"
                    f"Size: {size_mb:.2f} MB | Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')} | "
                    f"Data: {df.shape[0]} rows × {df.shape[1]} columns"
                )
            except Exception:
                self.info_label.setText(
                    f"Data: {df.shape[0]} rows × {df.shape[1]} columns")

        except Exception as e:
            self.status_label.setText(f"❌ Error loading file: {str(e)}")
            QMessageBox.critical(self, "Error Loading CSV",
                                 f"Failed to load CSV file:\n{str(e)}")

    def export_data(self):
        """Export the current data to a new CSV file"""
        if self.current_csv_data is None:
            QMessageBox.warning(self, "No Data", "No CSV data is loaded.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV Data", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_path:
            try:
                self.current_csv_data.to_csv(file_path, index=False)
                QMessageBox.information(
                    self, "Export Successful", f"Data exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error",
                                     f"Failed to export data:\n{str(e)}")


class CSVView(QWidget):
    """Main CSV view showing list of available CSV files"""

    def __init__(self, view_instance):
        super().__init__()
        self.view_instance = view_instance
        self.window = view_instance.window

        self.setup_ui()
        self.apply_theme_styling()
        self.load_csv_files()

    def setup_ui(self):
        """Setup the main CSV viewer UI"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(8)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title_label = QLabel("CSV Reports & Detection Logs")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Description
        self.desc_label = QLabel(
            "Click on any CSV file below to view its contents in a detailed viewer")
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.desc_label)

        # File list section
        self.create_file_list_section()

        # Control buttons
        self.create_control_buttons()

    def create_file_list_section(self):
        """Create the file list section"""
        # File list group with custom header
        file_group = QGroupBox()
        file_group_layout = QVBoxLayout(file_group)

        # Custom header with title and refresh icon
        header_layout = QHBoxLayout()

        # Title
        title_label = QLabel("Available CSV Files")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Refresh icon button
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.clicked.connect(self.load_csv_files)
        self.refresh_btn.setToolTip(
            "Refresh the list of CSV files from the reports directory")
        self.refresh_btn.setFixedSize(28, 28)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f8f9fa;
                font-size: 14px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #00ccff;
                border-color: #00ccff;
                color: white;
            }
            QPushButton:pressed {
                background-color: #00a3cc;
                color: white;
            }
        """)
        header_layout.addWidget(self.refresh_btn)

        file_group_layout.addLayout(header_layout)

        # File list
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.on_file_selected)
        self.file_list.setToolTip(
            "Double-click a file to open it in the CSV viewer")

        # Style will be applied by apply_theme_styling()

        file_group_layout.addWidget(self.file_list)

        # File info label
        self.file_info_label = QLabel("No files loaded yet")
        self.file_info_label.setWordWrap(True)
        self.file_info_label.setStyleSheet(
            "color: #666; font-size: 11px; padding: 5px;")
        file_group_layout.addWidget(self.file_info_label)

        self.main_layout.addWidget(file_group)

    def create_control_buttons(self):
        """Create control buttons"""
        button_layout = QHBoxLayout()

        # Browse for external CSV
        self.browse_btn = QPushButton("📁 Browse External CSV")
        self.browse_btn.clicked.connect(self.browse_external_csv)
        self.browse_btn.setToolTip("Open a CSV file from another location")
        button_layout.addWidget(self.browse_btn)

        button_layout.addStretch()

        # Info label
        info_label = QLabel(
            "💡 Tip: Double-click any CSV file to view its contents")
        info_label.setStyleSheet("color: #666; font-style: italic;")
        button_layout.addWidget(info_label)

        self.main_layout.addLayout(button_layout)

    def get_current_theme(self):
        """Get current theme from view instance"""
        try:
            if hasattr(self.view_instance, 'presenter') and self.view_instance.presenter:
                return getattr(self.view_instance.presenter.model.settings_model, 'theme', 'light')
        except (AttributeError, TypeError):
            pass
        return 'light'

    def apply_theme_styling(self):
        """Apply theme-aware styling to the main CSV view"""
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            # Dark theme colors - improved contrast
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            secondary_bg = "#404040"
            border_color = "#555555"
            list_bg = "#404040"
            list_alt_bg = "#454545"
            list_hover = "#505050"
            list_selected = "#00ccff"
        else:
            # Light theme colors - better contrast
            bg_color = "#FFFFFF"
            text_color = "#000000"
            secondary_bg = "#F8F9FA"
            border_color = "#E0E0E0"
            list_bg = "#FFFFFF"
            list_alt_bg = "#F8F9FA"
            list_hover = "#E9ECEF"
            list_selected = "#00ccff"

        # Apply main widget styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QLabel {{
                color: {text_color};
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
            
            QGroupBox {{
                font-weight: bold;
                border: none;
                margin: 0px;
                padding: 0px;
                background-color: transparent;
                color: {text_color};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 0px;
                padding: 0px;
                background-color: transparent;
                color: {text_color};
            }}
            
            QListWidget {{
                border: none;
                background-color: {list_bg};
                alternate-background-color: {list_alt_bg};
                color: {text_color};
                padding: 0px;
                margin: 0px;
            }}
            
            QListWidget::item {{
                padding: 4px;
                border: none;
                color: {text_color};
                margin: 0px;
            }}
            
            QListWidget::item:hover {{
                background-color: #00ccff;
                color: white;
            }}
            
            QListWidget::item:selected {{
                background-color: #00ccff;
                color: white;
            }}
            
            QPushButton {{
                background-color: {secondary_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 3px;
                padding: 4px 8px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: #00ccff;
                color: white;
                border-color: #00ccff;
            }}
            
            QPushButton:pressed {{
                background-color: #3A80D2;
                color: white;
            }}
        """)

        # Update description label color
        if hasattr(self, 'desc_label'):
            if current_theme == 'dark':
                self.desc_label.setStyleSheet(
                    "color: #CCCCCC; font-size: 14px;")
            else:
                self.desc_label.setStyleSheet(
                    "color: #666; font-size: 14px;")

        # Update file info label color
        if hasattr(self, 'file_info_label'):
            if current_theme == 'dark':
                self.file_info_label.setStyleSheet(
                    "color: #CCCCCC; font-size: 11px;")
            else:
                self.file_info_label.setStyleSheet(
                    "color: #666; font-size: 11px;")

    def load_csv_files(self):
        """Load CSV files from the reports directory specified in settings"""
        self.file_list.clear()

        try:
            # Get the report output path from settings
            if hasattr(self.view_instance, 'presenter') and self.view_instance.presenter:
                settings = self.view_instance.presenter.model.get_current_settings()
                report_path = settings.get(
                    'report_output_path', 'pyqt/reports')
            else:
                report_path = 'pyqt/reports'

            # Look for CSV files in the report directory
            csv_files = []
            if os.path.exists(report_path):
                pattern = report_path.replace("\\", "/") + "/*.csv"
                csv_files.extend(glob.glob(pattern))

            if not csv_files:
                # Create info item
                info_item = QListWidgetItem("📂 No CSV files found")
                info_item.setData(Qt.UserRole, None)
                info_item.setToolTip(f"No CSV files found in:\n{report_path}")
                info_item.setFlags(Qt.ItemIsEnabled)  # Make it non-selectable
                self.file_list.addItem(info_item)
                self.file_info_label.setText(
                    f"Searching in: {report_path}\nRun some predictions to generate CSV files!")
                return

            # Sort files by modification time (newest first)
            csv_files.sort(key=os.path.getmtime, reverse=True)

            for file_path in csv_files:
                filename = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                # Create display text with file info
                size_mb = file_size / (1024 * 1024)
                display_text = f"{filename}\n📊 {size_mb:.2f} MB • {mod_time.strftime('%Y-%m-%d %H:%M')}"

                # Create list item
                item = QListWidgetItem()
                item.setData(Qt.UserRole, file_path)
                item.setToolTip(
                    f"File: {filename}\nPath: {file_path}\nSize: {size_mb:.2f} MB\nModified: {mod_time}\n\nDouble-click to open")

                # Set icon and text based on file type
                if 'detection' in filename.lower():
                    item.setText(f"🔍 {display_text}")
                elif 'summary' in filename.lower():
                    item.setText(f"📋 {display_text}")
                else:
                    item.setText(f"📄 {display_text}")

                self.file_list.addItem(item)

            self.file_info_label.setText(
                f"Found {len(csv_files)} CSV files in: {report_path}")

        except Exception as e:
            error_item = QListWidgetItem(f"❌ Error loading files: {str(e)}")
            error_item.setData(Qt.UserRole, None)
            error_item.setFlags(Qt.ItemIsEnabled)  # Make it non-selectable
            self.file_list.addItem(error_item)
            self.file_info_label.setText(f"Error: {str(e)}")

    def on_file_selected(self, item):
        """Handle file selection from the list - open modal dialog"""
        file_path = item.data(Qt.UserRole)
        if file_path and os.path.exists(file_path):
            # Open modal dialog to view CSV data
            modal = CSVDataModal(file_path, self)
            modal.exec_()

    def browse_external_csv(self):
        """Browse for external CSV file and open it in modal"""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open External CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_path:
            # Open modal dialog to view CSV data
            modal = CSVDataModal(file_path, self)
            modal.exec_()

    def refresh_file_list(self):
        """Refresh the file list"""
        self.load_csv_files()
