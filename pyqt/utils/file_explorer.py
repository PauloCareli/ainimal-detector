import glob
import os
from datetime import datetime
from pathlib import Path

import cv2
from PIL import Image, ImageQt
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QComboBox, QDialog, QFileDialog, QGroupBox,
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QProgressBar, QPushButton, QVBoxLayout)


class ThumbnailGenerator(QThread):
    """Background thread for generating thumbnails"""

    thumbnail_ready = pyqtSignal(str, QPixmap)  # file_path, thumbnail
    progress_updated = pyqtSignal(int, int)  # current, total

    def __init__(self, file_paths, thumbnail_size=(120, 120)):
        super().__init__()
        self.file_paths = file_paths
        self.thumbnail_size = thumbnail_size
        self.is_running = True

    def run(self):
        """Generate thumbnails for all files"""
        total_files = len(self.file_paths)

        for i, file_path in enumerate(self.file_paths):
            if not self.is_running:
                break

            thumbnail = self.generate_thumbnail(file_path)
            if thumbnail:
                self.thumbnail_ready.emit(file_path, thumbnail)

            self.progress_updated.emit(i + 1, total_files)

    def generate_thumbnail(self, file_path):
        """Generate thumbnail for a single file"""
        try:
            file_ext = Path(file_path).suffix.lower()

            # Image files
            if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']:
                return self.generate_image_thumbnail(file_path)

            # Video files
            elif file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']:
                return self.generate_video_thumbnail(file_path)

            return None

        except Exception as e:
            print(f"Error generating thumbnail for {file_path}: {e}")
            return None

    def generate_image_thumbnail(self, image_path):
        """Generate thumbnail for image file"""
        try:
            # Use PIL for better format support
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()
                                  [-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb_img

                # Create thumbnail
                img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)

                # Convert to QPixmap
                qt_img = ImageQt.ImageQt(img)
                pixmap = QPixmap.fromImage(qt_img)

                return pixmap

        except Exception as e:
            print(f"Error creating image thumbnail: {e}")
            return None

    def generate_video_thumbnail(self, video_path):
        """Generate thumbnail for video file"""
        try:
            # Use OpenCV to extract first frame
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                return None

            # Read first frame
            ret, frame = cap.read()
            cap.release()

            if not ret:
                return None

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to PIL Image
            pil_img = Image.fromarray(frame_rgb)

            # Create thumbnail
            pil_img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)

            # Convert to QPixmap
            qt_img = ImageQt.ImageQt(pil_img)
            pixmap = QPixmap.fromImage(qt_img)

            return pixmap

        except Exception as e:
            print(f"Error creating video thumbnail: {e}")
            return None

    def stop(self):
        """Stop thumbnail generation"""
        self.is_running = False


class FileExplorerModal(QDialog):
    """Enhanced file explorer showing folder contents with thumbnails"""

    def __init__(self, initial_path="", parent=None):
        super().__init__(parent)
        self.selected_folder = initial_path
        self.thumbnails = {}  # Cache for thumbnails
        self.thumbnail_generator = None

        self.setup_ui()
        self.apply_styling()

        if initial_path and os.path.exists(initial_path):
            self.load_folder(initial_path)

    def setup_ui(self):
        """Setup the file explorer UI"""
        self.setWindowTitle("📁 Select Folder with Media Files")
        self.setModal(True)
        self.resize(900, 700)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header section
        self.create_header_section(main_layout)

        # File explorer section
        self.create_file_explorer_section(main_layout)

        # Progress bar for thumbnail generation
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        main_layout.addWidget(self.progress_bar)

        # Footer buttons
        self.create_footer_section(main_layout)

    def create_header_section(self, layout):
        """Create header with folder selection"""
        header_group = QGroupBox("Folder Selection")
        header_layout = QVBoxLayout(header_group)

        # Current folder display
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("No folder selected")
        self.folder_label.setWordWrap(True)
        self.folder_label.setStyleSheet(
            "font-weight: bold; color: #333; padding: 5px;")
        folder_layout.addWidget(self.folder_label, 1)

        # Browse button
        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(self.browse_folder)
        browse_btn.setToolTip("Select a different folder")
        folder_layout.addWidget(browse_btn)

        header_layout.addLayout(folder_layout)

        # Filter and count section
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Show:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "All Supported Files",
            "Images Only",
            "Videos Only"
        ])
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_combo)

        filter_layout.addStretch()

        self.file_count_label = QLabel("0 files")
        self.file_count_label.setStyleSheet("color: #666; font-weight: bold;")
        filter_layout.addWidget(self.file_count_label)

        header_layout.addLayout(filter_layout)
        layout.addWidget(header_group)

    def create_file_explorer_section(self, layout):
        """Create main file explorer with thumbnails"""
        explorer_group = QGroupBox("Folder Contents")
        explorer_layout = QVBoxLayout(explorer_group)

        # Info label
        self.info_label = QLabel("Select a folder to view its media files")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet(
            "color: #666; font-style: italic; padding: 20px;")
        explorer_layout.addWidget(self.info_label)

        # File list widget with grid view
        self.file_list = QListWidget()
        self.file_list.setIconSize(QSize(120, 120))
        self.file_list.setViewMode(QListWidget.IconMode)
        self.file_list.setResizeMode(QListWidget.Adjust)
        self.file_list.setSpacing(10)
        self.file_list.setUniformItemSizes(True)
        self.file_list.setWordWrap(True)

        # Hide the file list initially
        self.file_list.setVisible(False)
        explorer_layout.addWidget(self.file_list)

        layout.addWidget(explorer_group)

    def create_footer_section(self, layout):
        """Create footer buttons"""
        footer_layout = QHBoxLayout()

        # Info about current selection
        self.selection_info = QLabel("Select a folder to explore its contents")
        self.selection_info.setStyleSheet("color: #666; font-style: italic;")
        footer_layout.addWidget(self.selection_info)

        footer_layout.addStretch()

        # Confirm button
        self.confirm_btn = QPushButton("✅ Use This Folder")
        self.confirm_btn.clicked.connect(self.accept)
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.setToolTip("Use the selected folder for prediction")
        footer_layout.addWidget(self.confirm_btn)

        # Cancel button
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.clicked.connect(self.reject)
        footer_layout.addWidget(cancel_btn)

        layout.addLayout(footer_layout)

    def browse_folder(self):
        """Browse for a folder"""
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder", self.selected_folder or ""
        )
        if folder:
            self.load_folder(folder)

    def load_folder(self, folder_path):
        """Load folder contents"""
        try:
            self.selected_folder = folder_path
            self.folder_label.setText(f"📁 {folder_path}")
            self.confirm_btn.setEnabled(True)

            # Get supported file types
            image_extensions = ['.jpg', '.jpeg', '.png',
                                '.bmp', '.gif', '.tiff', '.webp']
            video_extensions = ['.mp4', '.avi', '.mov',
                                '.mkv', '.wmv', '.flv', '.webm']
            all_extensions = image_extensions + video_extensions

            # Find all supported files
            self.all_files = []
            for ext in all_extensions:
                pattern = os.path.join(folder_path, f"*{ext}")
                self.all_files.extend(glob.glob(pattern))
                # Also check uppercase
                pattern = os.path.join(folder_path, f"*{ext.upper()}")
                self.all_files.extend(glob.glob(pattern))

            # Sort files
            self.all_files.sort()

            if self.all_files:
                # Show file list and hide info label
                self.file_list.setVisible(True)
                self.info_label.setVisible(False)

                # Apply current filter
                self.apply_filter()

                # Start thumbnail generation
                self.start_thumbnail_generation()

                # Update info
                self.selection_info.setText(
                    f"Folder contains {len(self.all_files)} supported media files")
            else:
                # Hide file list and show info
                self.file_list.setVisible(False)
                self.info_label.setVisible(True)
                self.info_label.setText(
                    f"📂 No supported media files found in:\n{folder_path}\n\nSupported formats: JPG, PNG, MP4, AVI, MOV, etc.")
                self.file_count_label.setText("0 files")
                self.selection_info.setText(
                    "Selected folder contains no supported media files")

        except Exception as e:
            self.info_label.setText(f"❌ Error loading folder: {e}")
            self.selection_info.setText(f"Error: {e}")
            print(f"Error loading folder: {e}")

    def apply_filter(self):
        """Apply file type filter"""
        if not hasattr(self, 'all_files') or not self.all_files:
            return

        filter_type = self.filter_combo.currentText()

        image_extensions = ['.jpg', '.jpeg', '.png',
                            '.bmp', '.gif', '.tiff', '.webp']
        video_extensions = ['.mp4', '.avi', '.mov',
                            '.mkv', '.wmv', '.flv', '.webm']

        if filter_type == "Images Only":
            filtered_files = [f for f in self.all_files
                              if Path(f).suffix.lower() in image_extensions]
        elif filter_type == "Videos Only":
            filtered_files = [f for f in self.all_files
                              if Path(f).suffix.lower() in video_extensions]
        else:  # All Supported Files
            filtered_files = self.all_files

        self.populate_file_list(filtered_files)
        self.file_count_label.setText(f"{len(filtered_files)} files")

    def populate_file_list(self, files):
        """Populate the file list widget with files"""
        self.file_list.clear()

        if not files:
            return

        for file_path in files:
            file_name = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.lower()

            # Create list item
            item = QListWidgetItem()
            item.setText(file_name)
            item.setData(Qt.UserRole, file_path)

            # Calculate file info for tooltip
            try:
                file_size = os.path.getsize(file_path)
                size_mb = file_size / (1024 * 1024)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                tooltip = f"{file_name}\nSize: {size_mb:.2f} MB\nModified: {mod_time.strftime('%Y-%m-%d %H:%M')}\nPath: {file_path}"
            except:
                tooltip = f"{file_name}\nPath: {file_path}"

            item.setToolTip(tooltip)

            # Set default icon based on file type
            if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']:
                # Placeholder for images (will be replaced with thumbnail)
                item.setText(f"🖼️\n{file_name}")
            else:
                # Placeholder for videos (will be replaced with thumbnail)
                item.setText(f"🎥\n{file_name}")

            # Set text alignment
            item.setTextAlignment(Qt.AlignCenter)

            self.file_list.addItem(item)

    def start_thumbnail_generation(self):
        """Start generating thumbnails in background"""
        if self.thumbnail_generator and self.thumbnail_generator.isRunning():
            self.thumbnail_generator.stop()
            self.thumbnail_generator.wait()

        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Generating thumbnails... %p%")

        # Start thumbnail generation for current files
        current_files = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            file_path = item.data(Qt.UserRole)
            if file_path:
                current_files.append(file_path)

        if current_files:
            self.thumbnail_generator = ThumbnailGenerator(current_files)
            self.thumbnail_generator.thumbnail_ready.connect(
                self.on_thumbnail_ready)
            self.thumbnail_generator.progress_updated.connect(
                self.on_progress_updated)
            self.thumbnail_generator.finished.connect(
                self.on_thumbnail_generation_finished)
            self.thumbnail_generator.start()

    def on_thumbnail_ready(self, file_path, thumbnail):
        """Handle thumbnail ready signal"""
        self.thumbnails[file_path] = thumbnail

        # Update the list item with thumbnail
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.data(Qt.UserRole) == file_path:
                # Create scaled icon
                icon_size = self.file_list.iconSize()
                scaled_pixmap = thumbnail.scaled(
                    icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                # Set the icon and update text
                item.setIcon(QIcon(scaled_pixmap))
                item.setText(os.path.basename(file_path))
                break

    def on_progress_updated(self, current, total):
        """Handle progress update"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)

    def on_thumbnail_generation_finished(self):
        """Handle thumbnail generation completion"""
        self.progress_bar.setVisible(False)

    def get_selected_folder(self):
        """Get the selected folder path"""
        return self.selected_folder

    def apply_styling(self):
        """Apply consistent styling"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #f9f9f9;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: white;
            }
            
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                padding: 10px;
            }
            
            QListWidget::item {
                padding: 8px;
                border-radius: 8px;
                margin: 4px;
                background-color: #f8f9fa;
                border: 2px solid transparent;
            }
            
            QListWidget::item:selected {
                background-color: #e3f2fd;
                border: 2px solid #2196f3;
            }
            
            QListWidget::item:hover {
                background-color: #f0f8ff;
                border: 2px solid #87ceeb;
            }
            
            QPushButton {
                padding: 8px 16px;
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: white;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #f0f0f0;
                border-color: #999;
            }
            
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
            
            QComboBox {
                padding: 4px 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-width: 120px;
            }
        """)

    def closeEvent(self, event):
        """Handle close event"""
        if self.thumbnail_generator and self.thumbnail_generator.isRunning():
            self.thumbnail_generator.stop()
            self.thumbnail_generator.wait()
        event.accept()
