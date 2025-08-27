import glob
import os
from pathlib import Path

import cv2
from PIL import Image, ImageQt
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (QComboBox, QDialog, QFileDialog, QFrame,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget)


class ThumbnailGenerator(QThread):
    """Background thread for generating thumbnails"""

    thumbnail_ready = pyqtSignal(str, QPixmap)  # file_path, thumbnail
    progress_updated = pyqtSignal(int, int)  # current, total

    def __init__(self, file_paths, thumbnail_size=(150, 150)):
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


class ImageViewerDialog(QDialog):
    """Full-screen image viewer with navigation arrows"""

    def __init__(self, image_paths, current_index=0, parent=None):
        super().__init__(parent)
        self.image_paths = image_paths
        self.current_index = current_index
        self.setup_ui()
        self.load_current_image()

    def setup_ui(self):
        """Setup the image viewer UI"""
        self.setWindowTitle("Image Viewer")
        self.setModal(True)
        self.resize(1200, 800)  # Start with reasonable size, not maximized
        self.is_fullscreen = False

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Header with file info and controls
        header_layout = QHBoxLayout()

        # File info
        self.info_label = QLabel()
        self.info_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #333;")
        header_layout.addWidget(self.info_label)

        header_layout.addStretch()

        # Fullscreen button
        self.fullscreen_btn = QPushButton("⛶ Fullscreen")
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        self.fullscreen_btn.setFixedSize(100, 35)
        self.fullscreen_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ccff;
            }
        """)
        header_layout.addWidget(self.fullscreen_btn)

        layout.addLayout(header_layout)

        # Image display area with navigation
        image_layout = QHBoxLayout()

        # Previous button
        self.prev_btn = QPushButton("◀")
        self.prev_btn.clicked.connect(self.previous_image)
        self.prev_btn.setEnabled(
            self.current_index > 0 and len(self.image_paths) > 1)
        self.prev_btn.setFixedSize(50, 50)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ccff;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        image_layout.addWidget(self.prev_btn, 0, Qt.AlignVCenter)

        # Image display
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f9f9f9;
            }
        """)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)  # Larger minimum size
        self.image_label.setStyleSheet(
            "background-color: white; border-radius: 4px;")
        self.scroll_area.setWidget(self.image_label)

        image_layout.addWidget(self.scroll_area, 1)

        # Next button
        self.next_btn = QPushButton("▶")
        self.next_btn.clicked.connect(self.next_image)
        self.next_btn.setEnabled(self.current_index < len(
            self.image_paths) - 1 and len(self.image_paths) > 1)
        self.next_btn.setFixedSize(50, 50)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ccff;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        image_layout.addWidget(self.next_btn, 0, Qt.AlignVCenter)

        layout.addLayout(image_layout)

        # Footer with navigation info
        footer_layout = QHBoxLayout()

        # Keyboard shortcuts info
        shortcuts_label = QLabel(
            "Navigate: ← → Arrow Keys | Fullscreen: F11 | Close: Esc")
        shortcuts_label.setStyleSheet(
            "color: #666; font-size: 12px; font-style: italic;")
        footer_layout.addWidget(shortcuts_label)

        footer_layout.addStretch()

        # Image counter
        self.counter_label = QLabel()
        self.counter_label.setStyleSheet(
            "color: #666; font-size: 14px; font-weight: bold;")
        footer_layout.addWidget(self.counter_label)

        layout.addLayout(footer_layout)

        # Apply theme-aware styling
        self.apply_viewer_styling()

    def get_current_theme(self):
        """Get current theme from parent"""
        try:
            if hasattr(self, 'parent') and self.parent():
                if hasattr(self.parent(), 'get_current_theme'):
                    return self.parent().get_current_theme()
        except (AttributeError, TypeError):
            pass
        return 'light'

    def apply_viewer_styling(self):
        """Apply theme-aware styling to the viewer"""
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            # Dark theme colors
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            button_bg = "#404040"
            scroll_bg = "#353535"
        else:
            # Light theme colors
            bg_color = "#F5F5F5"
            text_color = "#333333"
            button_bg = "#FFFFFF"
            scroll_bg = "#F9F9F9"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QLabel {{
                color: {text_color};
                background-color: transparent;
            }}
            
            QPushButton {{
                color: {text_color};
            }}
            
            QScrollArea {{
                background-color: {scroll_bg};
            }}
        """)

    def load_current_image(self):
        """Load and display the current image"""
        if not self.image_paths or self.current_index >= len(self.image_paths):
            return

        file_path = self.image_paths[self.current_index]
        file_name = os.path.basename(file_path)

        try:
            # Update info and counter labels
            self.info_label.setText(f"📷 {file_name}")
            self.counter_label.setText(
                f"{self.current_index + 1} / {len(self.image_paths)}")

            # Load image
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Get original image size
                original_size = pixmap.size()

                # Get available space in the dialog (accounting for buttons and headers)
                available_width = self.width() - 150  # Account for nav buttons and margins
                available_height = self.height() - 120  # Account for header and footer

                # Use minimum of available space and 1920x1080
                max_width = min(available_width, 1920)
                max_height = min(available_height, 1080)
                max_size = QSize(max_width, max_height)

                # Scale image to fit the available space while maintaining aspect ratio
                if original_size.width() > max_size.width() or original_size.height() > max_size.height():
                    scaled_pixmap = pixmap.scaled(
                        max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                else:
                    # For smaller images, scale them up to use more space (but not beyond original)
                    scale_factor = min(
                        max_size.width() / original_size.width(),
                        max_size.height() / original_size.height(),
                        2.0  # Don't scale up more than 2x
                    )
                    if scale_factor > 1.0:
                        new_size = QSize(
                            int(original_size.width() * scale_factor),
                            int(original_size.height() * scale_factor)
                        )
                        scaled_pixmap = pixmap.scaled(
                            new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    else:
                        scaled_pixmap = pixmap

                self.image_label.setPixmap(scaled_pixmap)

                # Update image label size to match the scaled image
                self.image_label.resize(scaled_pixmap.size())
            else:
                self.image_label.setText(
                    f"❌ Unable to load image:\n{file_name}")

            # Update navigation button states
            self.prev_btn.setEnabled(self.current_index > 0)
            self.next_btn.setEnabled(
                self.current_index < len(self.image_paths) - 1)

        except Exception as e:
            self.image_label.setText(f"❌ Error loading image:\n{e}")

    def previous_image(self):
        """Go to previous image"""
        print(
            f"Previous clicked: current_index={self.current_index}, total={len(self.image_paths)}")
        if self.current_index > 0:
            self.current_index -= 1
            print(f"Moving to previous image: new_index={self.current_index}")
            self.load_current_image()
        else:
            print("Already at first image")

    def next_image(self):
        """Go to next image"""
        print(
            f"Next clicked: current_index={self.current_index}, total={len(self.image_paths)}")
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            print(f"Moving to next image: new_index={self.current_index}")
            self.load_current_image()
        else:
            print("Already at last image")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.is_fullscreen:
            self.showNormal()
            self.resize(1200, 800)
            self.fullscreen_btn.setText("⛶ Fullscreen")
            self.is_fullscreen = False
        else:
            self.showMaximized()
            self.fullscreen_btn.setText("⛶ Exit Fullscreen")
            self.is_fullscreen = True

        # Reload the current image to take advantage of new size
        self.load_current_image()

        # Refresh styling in case theme changed
        self.apply_viewer_styling()

    def keyPressEvent(self, event):
        """Handle keyboard navigation"""
        if event.key() == Qt.Key_Left:
            self.previous_image()
        elif event.key() == Qt.Key_Right:
            self.next_image()
        elif event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        super().keyPressEvent(event)


class ImageView(QWidget):
    """Modern image gallery view with thumbnails and expansion"""

    def __init__(self, view_instance):
        super(ImageView, self).__init__()
        self.view_instance = view_instance
        self.window = view_instance.window
        self.current_folder = ""
        self.all_files = []
        self.filtered_files = []
        self.thumbnails = {}
        self.thumbnail_generator = None

        self.setup_ui()
        self.apply_styling()

    def setup_ui(self):
        """Setup the modern gallery UI"""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title_label = QLabel("🖼️ Image & Video Gallery")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title_label)

        # Controls section
        self.create_controls_section()

        # Gallery section
        self.create_gallery_section()

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        self.main_layout.addWidget(self.progress_bar)

    def create_controls_section(self):
        """Create folder selection and filter controls"""
        controls_group = QGroupBox("Gallery Controls")
        controls_layout = QVBoxLayout(controls_group)

        # Folder selection
        folder_layout = QHBoxLayout()

        folder_layout.addWidget(QLabel("📁 Folder:"))

        self.folder_label = QLabel(
            "No folder selected - Click 'Select Folder' to browse images")
        self.folder_label.setStyleSheet(
            "font-weight: bold; color: #555; padding: 8px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 4px;")
        self.folder_label.setWordWrap(True)
        folder_layout.addWidget(self.folder_label, 1)

        self.select_folder_btn = QPushButton("📁 Select Folder")
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.select_folder_btn.setToolTip(
            "Select a folder containing images and videos")
        folder_layout.addWidget(self.select_folder_btn)

        controls_layout.addLayout(folder_layout)

        # Filter and info
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("🔍 Filter:"))

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
        self.file_count_label.setStyleSheet(
            "color: #666; font-weight: bold; font-size: 14px;")
        filter_layout.addWidget(self.file_count_label)

        controls_layout.addLayout(filter_layout)

        self.main_layout.addWidget(controls_group)

    def create_gallery_section(self):
        """Create the thumbnail gallery"""
        gallery_group = QGroupBox("Gallery")
        gallery_layout = QVBoxLayout(gallery_group)

        # Info label for empty state
        self.gallery_info = QLabel(
            "📂 Select a folder to view your images and videos\n\nSupported formats: JPG, PNG, MP4, AVI, MOV, and more!")
        self.gallery_info.setAlignment(Qt.AlignCenter)
        self.gallery_info.setStyleSheet("""
            QLabel {
                color: #666; 
                font-style: italic; 
                font-size: 16px;
                padding: 60px;
                background-color: #f9f9f9;
                border: 2px dashed #ccc;
                border-radius: 8px;
            }
        """)
        gallery_layout.addWidget(self.gallery_info)

        # Thumbnail grid
        self.gallery_scroll = QScrollArea()
        self.gallery_scroll.setWidgetResizable(True)
        self.gallery_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.gallery_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.gallery_widget = QWidget()
        self.gallery_layout = QGridLayout(self.gallery_widget)
        self.gallery_layout.setSpacing(8)
        self.gallery_layout.setContentsMargins(5, 5, 5, 5)

        self.gallery_scroll.setWidget(self.gallery_widget)
        self.gallery_scroll.setVisible(False)
        gallery_layout.addWidget(self.gallery_scroll)

        self.main_layout.addWidget(gallery_group)

    def select_folder(self):
        """Open folder selection dialog"""
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Select Folder with Images/Videos")
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)

        # Set file filters
        filters = [
            "All Files (*)",
            "Images (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp)",
            "Videos (*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm)",
            "Images and Videos (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm)"
        ]
        dialog.setNameFilters(filters)
        dialog.selectNameFilter(
            "Images and Videos (*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp *.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm)")

        if self.current_folder and os.path.exists(self.current_folder):
            dialog.setDirectory(self.current_folder)

        if dialog.exec_() == QFileDialog.Accepted:
            selected_paths = dialog.selectedFiles()
            if selected_paths:
                selected_path = selected_paths[0]

                # If a file was selected, get its parent directory
                if os.path.isfile(selected_path):
                    folder_path = os.path.dirname(selected_path)
                else:
                    folder_path = selected_path

                self.load_folder(folder_path)

    def load_folder(self, folder_path):
        """Load images from the selected folder"""
        try:
            self.current_folder = folder_path
            self.folder_label.setText(f"📁 {folder_path}")

            # Get supported file types
            image_extensions = ['.jpg', '.jpeg', '.png',
                                '.bmp', '.gif', '.tiff', '.webp']
            video_extensions = ['.mp4', '.avi', '.mov',
                                '.mkv', '.wmv', '.flv', '.webm']
            all_extensions = image_extensions + video_extensions

            # Find all supported files
            self.all_files = []
            for ext in all_extensions:
                # Use case-insensitive pattern
                pattern = os.path.join(folder_path, f"*{ext}")
                files_found = glob.glob(pattern, recursive=False)
                # Also check uppercase
                pattern_upper = os.path.join(folder_path, f"*{ext.upper()}")
                files_found.extend(glob.glob(pattern_upper, recursive=False))
                self.all_files.extend(files_found)

            # Remove duplicates (in case of case-insensitive filesystem)
            self.all_files = list(set(self.all_files))

            # Sort files
            self.all_files.sort()

            if self.all_files:
                # Show gallery and hide info label
                self.gallery_scroll.setVisible(True)
                self.gallery_info.setVisible(False)

                # Apply current filter
                self.apply_filter()

                # Start thumbnail generation
                self.start_thumbnail_generation()
            else:
                # Hide gallery and show info
                self.gallery_scroll.setVisible(False)
                self.gallery_info.setVisible(True)
                self.gallery_info.setText(
                    f"📂 No supported media files found in:\n{folder_path}\n\nSupported formats: JPG, PNG, MP4, AVI, MOV, etc.")
                self.file_count_label.setText("0 files")

        except Exception as e:
            self.gallery_info.setText(f"❌ Error loading folder: {e}")
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

        # Store current filtered files
        self.filtered_files = filtered_files

        self.populate_gallery(filtered_files)
        self.file_count_label.setText(f"{len(filtered_files)} files")

    def populate_gallery(self, files):
        """Populate the gallery with file thumbnails"""
        # Clear existing thumbnails
        self.clear_gallery()

        if not files:
            return

        # Calculate grid dimensions
        columns = 4  # Number of thumbnails per row

        for i, file_path in enumerate(files):
            row = i // columns
            col = i % columns

            # Create thumbnail item
            item_widget = self.create_thumbnail_item(file_path)
            self.gallery_layout.addWidget(item_widget, row, col)

    def create_thumbnail_item(self, file_path):
        """Create a thumbnail item widget"""
        item_frame = QFrame()
        item_frame.setFrameStyle(QFrame.Box)
        item_frame.setFixedSize(200, 220)
        item_layout = QVBoxLayout(item_frame)
        item_layout.setContentsMargins(5, 5, 5, 5)

        # Thumbnail label
        thumb_label = QLabel()
        thumb_label.setFixedSize(180, 160)
        thumb_label.setAlignment(Qt.AlignCenter)
        thumb_label.setStyleSheet("""
            QLabel {
                border: 1px solid #ddd;
                background-color: #f9f9f9;
                border-radius: 4px;
                padding: 2px;
            }
        """)

        # Set default icon based on file type
        file_ext = Path(file_path).suffix.lower()
        if file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']:
            thumb_label.setText("🖼️\nLoading\nPreview...")
        else:
            thumb_label.setText("🎥\nLoading\nPreview...")

        # Make clickable
        thumb_label.mousePressEvent = lambda event, path=file_path: self.open_image_viewer(
            path)
        thumb_label.setCursor(Qt.PointingHandCursor)

        item_layout.addWidget(thumb_label)

        # File name label
        file_name = os.path.basename(file_path)
        if len(file_name) > 18:
            display_name = file_name[:15] + "..."
        else:
            display_name = file_name

        name_label = QLabel(display_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setToolTip(f"Click to view: {file_path}")
        name_label.setWordWrap(True)
        name_label.setMaximumHeight(40)
        name_label.setStyleSheet(
            "font-size: 11px; color: #333; font-weight: bold;")
        item_layout.addWidget(name_label)

        # Store reference for thumbnail updates
        thumb_label.setProperty("file_path", file_path)

        return item_frame

    def clear_gallery(self):
        """Clear all thumbnail items from gallery"""
        while self.gallery_layout.count():
            child = self.gallery_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

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
        if hasattr(self, 'filtered_files') and self.filtered_files:
            self.thumbnail_generator = ThumbnailGenerator(self.filtered_files)
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

        # Find and update the corresponding thumbnail label
        for i in range(self.gallery_layout.count()):
            item = self.gallery_layout.itemAt(i)
            if item and item.widget():
                frame = item.widget()
                # Look for the thumbnail label specifically (first QLabel child)
                for child in frame.findChildren(QLabel):
                    if child.property("file_path") == file_path:
                        # Scale thumbnail to fit the label size
                        label_size = child.size()
                        if label_size.width() > 0 and label_size.height() > 0:
                            scaled_thumbnail = thumbnail.scaled(
                                label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            child.setPixmap(scaled_thumbnail)
                        break

    def on_progress_updated(self, current, total):
        """Handle progress update"""
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)

    def on_thumbnail_generation_finished(self):
        """Handle thumbnail generation completion"""
        self.progress_bar.setVisible(False)

    def open_image_viewer(self, file_path):
        """Open the full-screen image viewer"""
        if not self.filtered_files:
            return

        # Filter to only image files for the viewer (videos not supported in viewer yet)
        image_extensions = ['.jpg', '.jpeg', '.png',
                            '.bmp', '.gif', '.tiff', '.webp']
        image_files = [f for f in self.filtered_files
                       if Path(f).suffix.lower() in image_extensions]

        if not image_files:
            return

        # Find current image index
        try:
            current_index = image_files.index(file_path)
        except ValueError:
            current_index = 0

        # Open image viewer
        viewer = ImageViewerDialog(image_files, current_index, self)
        viewer.exec_()

    def get_current_theme(self):
        """Get current theme from view instance"""
        try:
            if hasattr(self, 'view_instance') and self.view_instance:
                if hasattr(self.view_instance, 'presenter') and self.view_instance.presenter:
                    return getattr(self.view_instance.presenter.model.settings_model, 'theme', 'light')
        except (AttributeError, TypeError):
            pass
        return 'light'

    def apply_styling(self):
        """Apply consistent styling"""
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            # Dark theme colors
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            secondary_bg = "#404040"
            border_color = "#666666"
            group_bg = "#353535"
            button_bg = "#404040"
            button_hover = "#00ccff"
        else:
            # Light theme colors
            bg_color = "#FFFFFF"
            text_color = "#000000"
            secondary_bg = "#F8F9FA"
            border_color = "#DEE2E6"
            group_bg = "#FAFAFA"
            button_bg = "#FFFFFF"
            button_hover = "#00ccff"

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QLabel {{
                color: {text_color};
                background-color: transparent;
            }}
            
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {border_color};
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: {group_bg};
                color: {text_color};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px 0 6px;
                background-color: {bg_color};
                color: {text_color};
                font-size: 14px;
            }}
            
            QPushButton {{
                padding: 10px 20px;
                font-weight: bold;
                border: 1px solid {border_color};
                border-radius: 6px;
                background-color: {button_bg};
                color: {text_color};
                min-width: 120px;
                font-size: 13px;
            }}
            
            QPushButton:hover {{
                background-color: {button_hover};
                border-color: {button_hover};
                color: white;
            }}
            
            QPushButton:pressed {{
                background-color: #3A80D2;
                color: white;
            }}
            
            QComboBox {{
                padding: 6px 12px;
                border: 1px solid {border_color};
                border-radius: 6px;
                background-color: {button_bg};
                color: {text_color};
                min-width: 150px;
                font-size: 13px;
            }}
            
            QComboBox:hover {{
                border-color: {button_hover};
            }}
            
            QComboBox::drop-down {{
                border: none;
                background-color: transparent;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border: none;
                width: 12px;
                height: 12px;
            }}
            
            QFrame {{
                border: 1px solid {border_color};
                border-radius: 6px;
                background-color: {button_bg};
                margin: 2px;
            }}
            
            QFrame:hover {{
                border-color: {button_hover};
                background-color: {secondary_bg};
            }}
            
            QScrollArea {{
                border: 1px solid {border_color};
                border-radius: 6px;
                background-color: {bg_color};
            }}
            
            QProgressBar {{
                border: 1px solid {border_color};
                border-radius: 4px;
                text-align: center;
                background-color: {secondary_bg};
                color: {text_color};
            }}
            
            QProgressBar::chunk {{
                background-color: #4CAF50;
                border-radius: 3px;
            }}
        """)

    def closeEvent(self, event):
        """Handle close event"""
        if self.thumbnail_generator and self.thumbnail_generator.isRunning():
            self.thumbnail_generator.stop()
            self.thumbnail_generator.wait()
        event.accept()
