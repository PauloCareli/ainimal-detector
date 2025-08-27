from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont


class CustomModal(QDialog):
    """Custom modal dialog to replace standard QMessageBox with themed design"""

    # Modal types
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    QUESTION = "question"

    # Signals
    accepted = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self, modal_type=INFO, title="", message="", details="",
                 parent=None, auto_close=False, auto_close_delay=3000,
                 show_cancel=False, custom_buttons=None):
        super().__init__(parent)

        self.modal_type = modal_type
        self.title_text = title
        self.message_text = message
        self.details_text = details
        self.auto_close = auto_close
        self.auto_close_delay = auto_close_delay
        self.show_cancel = show_cancel
        self.custom_buttons = custom_buttons or []

        self.setup_ui()
        self.apply_styling()

        # Auto-close timer for success messages
        if self.auto_close:
            self.auto_close_timer = QTimer()
            self.auto_close_timer.timeout.connect(self.accept)
            self.auto_close_timer.start(self.auto_close_delay)

    def setup_ui(self):
        """Setup the modal UI"""
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Content frame with shadow
        self.content_frame = QFrame()
        self.content_frame.setFrameStyle(QFrame.StyledPanel)
        self.content_frame.setObjectName("contentFrame")

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(Qt.black)
        self.content_frame.setGraphicsEffect(shadow)

        # Content layout
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(30, 25, 30, 25)

        # Header section
        self.create_header_section(content_layout)

        # Message section
        self.create_message_section(content_layout)

        # Details section (if provided)
        if self.details_text:
            self.create_details_section(content_layout)

        # Buttons section
        self.create_buttons_section(content_layout)

        main_layout.addWidget(self.content_frame)

        # Set size constraints
        self.setMinimumWidth(400)
        self.setMaximumWidth(600)
        self.adjustSize()

        # Center on parent or screen
        if self.parent():
            self.move(
                self.parent().x() + (self.parent().width() - self.width()) // 2,
                self.parent().y() + (self.parent().height() - self.height()) // 2
            )

    def create_header_section(self, layout):
        """Create header with icon and title"""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(48, 48)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.set_modal_icon()
        header_layout.addWidget(self.icon_label)

        # Title
        if self.title_text:
            self.title_label = QLabel(self.title_text)
            title_font = QFont()
            title_font.setPointSize(16)
            title_font.setBold(True)
            self.title_label.setFont(title_font)
            self.title_label.setWordWrap(True)
            header_layout.addWidget(self.title_label, 1)

        layout.addLayout(header_layout)

    def create_message_section(self, layout):
        """Create main message section"""
        if self.message_text:
            self.message_label = QLabel(self.message_text)
            message_font = QFont()
            message_font.setPointSize(12)
            self.message_label.setFont(message_font)
            self.message_label.setWordWrap(True)
            self.message_label.setAlignment(Qt.AlignLeft)
            layout.addWidget(self.message_label)

    def create_details_section(self, layout):
        """Create expandable details section"""
        self.details_text_edit = QTextEdit()
        self.details_text_edit.setPlainText(self.details_text)
        self.details_text_edit.setReadOnly(True)
        self.details_text_edit.setMaximumHeight(150)
        self.details_text_edit.setMinimumHeight(80)
        layout.addWidget(self.details_text_edit)

    def create_buttons_section(self, layout):
        """Create buttons section"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()

        # Custom buttons if provided
        if self.custom_buttons:
            for button_text, callback in self.custom_buttons:
                btn = QPushButton(button_text)
                btn.clicked.connect(callback)
                btn.clicked.connect(self.accept)
                self.style_button(btn, "primary" if button_text.lower() in [
                                  "ok", "yes", "save"] else "secondary")
                button_layout.addWidget(btn)
        else:
            # Default buttons based on modal type
            if self.modal_type == self.QUESTION:
                # Yes/No buttons
                yes_btn = QPushButton("Yes")
                yes_btn.clicked.connect(self.accept)
                self.style_button(yes_btn, "primary")
                button_layout.addWidget(yes_btn)

                no_btn = QPushButton("No")
                no_btn.clicked.connect(self.reject)
                self.style_button(no_btn, "secondary")
                button_layout.addWidget(no_btn)
            else:
                # OK button
                ok_btn = QPushButton("OK")
                ok_btn.clicked.connect(self.accept)
                ok_btn.setDefault(True)
                self.style_button(ok_btn, "primary")
                button_layout.addWidget(ok_btn)

                # Optional Cancel button
                if self.show_cancel:
                    cancel_btn = QPushButton("Cancel")
                    cancel_btn.clicked.connect(self.reject)
                    self.style_button(cancel_btn, "secondary")
                    button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)

    def set_modal_icon(self):
        """Set icon based on modal type"""
        icons = {
            self.SUCCESS: "✅",
            self.ERROR: "❌",
            self.WARNING: "⚠️",
            self.INFO: "ℹ️",
            self.QUESTION: "❓"
        }

        icon_text = icons.get(self.modal_type, "ℹ️")
        self.icon_label.setText(icon_text)
        self.icon_label.setStyleSheet("font-size: 32px;")

    def get_current_theme(self):
        """Get current theme from parent if available"""
        try:
            # Try to get theme from parent view
            if self.parent() and hasattr(self.parent(), 'get_current_theme'):
                return self.parent().get_current_theme()
            elif self.parent() and hasattr(self.parent(), 'view_instance'):
                view_instance = self.parent().view_instance
                if hasattr(view_instance, 'presenter') and view_instance.presenter:
                    return getattr(view_instance.presenter.model.settings_model, 'theme', 'light')
        except (AttributeError, TypeError):
            pass
        return 'light'

    def style_button(self, button, button_type="primary"):
        """Apply consistent styling to buttons"""
        current_theme = self.get_current_theme()

        if current_theme == 'dark':
            if button_type == "primary":
                bg_color = "#00ccff"
                text_color = "#000000"
                hover_bg = "#66D9FF"
            else:
                bg_color = "#555555"
                text_color = "#FFFFFF"
                hover_bg = "#666666"
        else:
            if button_type == "primary":
                bg_color = "#2196F3"
                text_color = "#FFFFFF"
                hover_bg = "#1976D2"
            else:
                bg_color = "#E0E0E0"
                text_color = "#000000"
                hover_bg = "#CCCCCC"

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
            }}
            QPushButton:pressed {{
                background-color: {bg_color};
                padding: 11px 19px 9px 21px;
            }}
        """)

    def apply_styling(self):
        """Apply theme-aware styling to the modal"""
        current_theme = self.get_current_theme()

        # Color scheme based on modal type and theme
        if current_theme == 'dark':
            bg_color = "#2E2E2E"
            text_color = "#FFFFFF"
            border_color = "#555555"
            accent_colors = {
                self.SUCCESS: "#00ccff",
                self.ERROR: "#F44336",
                self.WARNING: "#FF9800",
                self.INFO: "#00ccff",
                self.QUESTION: "#9C27B0"
            }
        else:
            bg_color = "#FFFFFF"
            text_color = "#000000"
            border_color = "#E0E0E0"
            accent_colors = {
                self.SUCCESS: "#00ccff",
                self.ERROR: "#F44336",
                self.WARNING: "#FF9800",
                self.INFO: "#00ccff",
                self.QUESTION: "#9C27B0"
            }

        accent_color = accent_colors.get(
            self.modal_type, accent_colors[self.INFO])

        # Apply main styling
        self.setStyleSheet(f"""
            QDialog {{
                background-color: transparent;
            }}
            
            QFrame#contentFrame {{
                background-color: {bg_color};
                border: 2px solid {accent_color};
                border-radius: 12px;
            }}
            
            QLabel {{
                color: {text_color};
                background-color: transparent;
            }}
            
            QTextEdit {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 8px;
                font-size: 11px;
            }}
        """)

        # Style title with accent color
        if hasattr(self, 'title_label'):
            self.title_label.setStyleSheet(f"color: {accent_color};")

    def accept(self):
        """Override accept to emit custom signal"""
        self.accepted.emit()
        super().accept()

    def reject(self):
        """Override reject to emit custom signal"""
        self.rejected.emit()
        super().reject()

    def closeEvent(self, event):
        """Handle close event"""
        if hasattr(self, 'auto_close_timer'):
            self.auto_close_timer.stop()
        event.accept()


class ModalManager:
    """Helper class for showing different types of modals"""

    @staticmethod
    def show_success(title, message, parent=None, auto_close=True, auto_close_delay=3000):
        """Show success modal"""
        modal = CustomModal(
            modal_type=CustomModal.SUCCESS,
            title=title,
            message=message,
            parent=parent,
            auto_close=auto_close,
            auto_close_delay=auto_close_delay
        )
        return modal.exec_()

    @staticmethod
    def show_error(title, message, details="", parent=None):
        """Show error modal"""
        modal = CustomModal(
            modal_type=CustomModal.ERROR,
            title=title,
            message=message,
            details=details,
            parent=parent
        )
        return modal.exec_()

    @staticmethod
    def show_warning(title, message, parent=None, show_cancel=False):
        """Show warning modal"""
        modal = CustomModal(
            modal_type=CustomModal.WARNING,
            title=title,
            message=message,
            parent=parent,
            show_cancel=show_cancel
        )
        return modal.exec_()

    @staticmethod
    def show_info(title, message, parent=None):
        """Show info modal"""
        modal = CustomModal(
            modal_type=CustomModal.INFO,
            title=title,
            message=message,
            parent=parent
        )
        return modal.exec_()

    @staticmethod
    def show_question(title, message, parent=None):
        """Show question modal with Yes/No buttons"""
        modal = CustomModal(
            modal_type=CustomModal.QUESTION,
            title=title,
            message=message,
            parent=parent
        )
        result = modal.exec_()
        return result == QDialog.Accepted

    @staticmethod
    def show_custom(title, message, buttons, parent=None, modal_type=CustomModal.INFO):
        """Show custom modal with custom buttons"""
        modal = CustomModal(
            modal_type=modal_type,
            title=title,
            message=message,
            parent=parent,
            custom_buttons=buttons
        )
        return modal.exec_()
