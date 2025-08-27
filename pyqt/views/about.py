from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QFont
from PyQt5.QtWidgets import (QFrame, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QPushButton, QScrollArea, QVBoxLayout,
                             QWidget)


class AboutView(QWidget):
    def __init__(self, view_instance):
        super(AboutView, self).__init__()
        self.view_instance = view_instance
        self.setup_ui()
        self.apply_styling()

    def setup_ui(self):
        """Setup the modern about page UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for the content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(40, 40, 40, 40)

        # Header section
        self.create_header_section(content_layout)

        # Features section
        self.create_features_section(content_layout)

        # Author section
        self.create_author_section(content_layout)

        # Footer section
        self.create_footer_section(content_layout)

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def create_header_section(self, layout):
        """Create the header section with logo and title"""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(20)

        # App icon/logo placeholder
        icon_label = QLabel("🦁")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 64px;")
        header_layout.addWidget(icon_label)

        # App title
        title_label = QLabel("AInimal Detector")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        # Version and description
        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(version_label)

        description_label = QLabel(
            "Advanced AI-powered animal detection system using self-trained YOLO deep learning models\n"
            "for wildlife monitoring and camera trap analysis"
        )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        header_layout.addWidget(description_label)

        layout.addWidget(header_frame)

    def create_features_section(self, layout):
        """Create features section"""
        features_group = QGroupBox("🚀 Key Features")
        features_layout = QGridLayout(features_group)
        features_layout.setSpacing(15)

        features = [
            ("🤖 AI Detection", "Self-trained YOLO models for accurate animal detection"),
            ("📷 Multi-Media", "Support for images and videos with batch processing"),
            ("📊 CSV Reports", "Detailed detection logs with timestamps and coordinates"),
            ("🎨 Modern UI", "Clean, responsive interface with light/dark themes"),
            ("⚡ High Performance", "Optimized for speed with GPU acceleration support"),
            ("📈 Analytics", "Visual detection statistics and confidence scoring")
        ]

        for i, (title, desc) in enumerate(features):
            row = i // 2
            col = i % 2

            feature_frame = QFrame()
            feature_layout = QVBoxLayout(feature_frame)
            feature_layout.setSpacing(5)

            title_label = QLabel(title)
            title_font = QFont()
            title_font.setBold(True)
            title_font.setPointSize(12)
            title_label.setFont(title_font)
            feature_layout.addWidget(title_label)

            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            feature_layout.addWidget(desc_label)

            features_layout.addWidget(feature_frame, row, col)

        layout.addWidget(features_group)

    def create_author_section(self, layout):
        """Create author and contact section"""
        author_group = QGroupBox("About the Developer")
        author_layout = QVBoxLayout(author_group)
        author_layout.setSpacing(15)

        # Author info
        author_info = QLabel(
            "<span style='font-size: 18px; font-weight: bold;'>Paulo Careli</span><br/>"
            "Software Engineer<br/>"
        )
        author_info.setAlignment(Qt.AlignCenter)
        author_layout.addWidget(author_info)

        # Contact buttons
        contact_layout = QHBoxLayout()
        contact_layout.setSpacing(15)

        # LinkedIn button
        linkedin_btn = QPushButton("🔗 LinkedIn Profile")
        linkedin_btn.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://www.linkedin.com/in/paulo-careli/")))
        contact_layout.addWidget(linkedin_btn)

        # GitHub button
        github_btn = QPushButton("📂 GitHub Project")
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://github.com/PauloCareli/camera-trap-animal-detection-with-deep-learning")))
        contact_layout.addWidget(github_btn)

        # Email button
        email_btn = QPushButton("📧 Send Email")
        email_btn.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("mailto:paulohcareli@gmail.com?subject=AInimal Detector - Contact")))
        contact_layout.addWidget(email_btn)

        author_layout.addLayout(contact_layout)
        layout.addWidget(author_group)

    def create_footer_section(self, layout):
        """Create footer section"""
        footer_frame = QFrame()
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setSpacing(10)

        # License info
        license_label = QLabel(
            "📄 <b>License:</b> This software is provided as-is for educational and research purposes.<br/>"
            "🌟 <b>Open Source:</b> Source code available on GitHub under GNU General Public License.<br/>"
            "🙏 <b>Acknowledgments:</b> Thanks to Ultralytics for YOLO, OpenCV community, and PyQt developers."
        )
        license_label.setWordWrap(True)
        license_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(license_label)

        # Copyright
        copyright_label = QLabel("© 2024 Paulo Careli. All rights reserved.")
        copyright_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(copyright_label)

        layout.addWidget(footer_frame)

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
        """Apply theme-aware styling"""
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
            scroll_bg = "#2E2E2E"
        else:
            # Light theme colors
            bg_color = "#FFFFFF"
            text_color = "#000000"
            secondary_bg = "#F8F9FA"
            border_color = "#DEE2E6"
            group_bg = "#FAFAFA"
            button_bg = "#FFFFFF"
            button_hover = "#00ccff"
            scroll_bg = "#FFFFFF"

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
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: {group_bg};
                color: {text_color};
                font-size: 14px;
            }}

            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: {bg_color};
                color: {text_color};
                font-size: 16px;
            }}

            QPushButton {{
                background-color: {button_bg};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 120px;
            }}

            QPushButton:hover {{
                background-color: {button_hover};
                color: white;
                border-color: {button_hover};
            }}

            QPushButton:pressed {{
                background-color: #00a3cc;
                color: white;
            }}

            QFrame {{
                border: none;
                background-color: transparent;
            }}

            QScrollArea {{
                border: none;
                background-color: {scroll_bg};
            }}

            QScrollBar:vertical {{
                border: none;
                background-color: {secondary_bg};
                width: 12px;
                border-radius: 6px;
            }}

            QScrollBar::handle:vertical {{
                background-color: {border_color};
                border-radius: 6px;
                min-height: 20px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {button_hover};
            }}
        """)

    def refresh_styling(self):
        """Refresh styling when theme changes"""
        self.apply_styling()
