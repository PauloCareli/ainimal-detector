try:
    from PyQt5.QtWidgets import QMessageBox
except ImportError:
    # Fallback in case PyQt5 is not available during linting
    QMessageBox = None


class SettingsPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect the config view signal to save settings
        self.view.config_view.settings_saved.connect(self.save_settings)

        # Load current settings into the UI
        self.load_settings_to_ui()

    def load_settings_to_ui(self):
        """Load current settings from model into the UI"""
        current_settings = self.model.get_current_settings()
        self.view.config_view.load_settings(current_settings)

    def save_settings(self, settings):
        """Save settings through the model"""
        try:
            # Store the old theme to check if it changed
            old_theme = self.model.settings_model.theme

            # Save the settings
            success = self.model.save_settings(settings)

            if success:
                # Apply theme change if needed BEFORE showing the message
                new_theme = settings.get("theme")
                if new_theme and new_theme != old_theme:
                    self.apply_theme_change(new_theme)

                # Show success message
                if QMessageBox:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Settings Saved")
                    msg.setText("Settings have been saved successfully!")
                    msg.exec_()

                print("Settings saved and applied successfully")

            elif QMessageBox:
                # Show error message
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Save Failed")
                msg.setText("Failed to save settings. Please try again.")
                msg.exec_()

        except (ValueError, KeyError, FileNotFoundError) as e:
            # Show error message for specific exceptions
            if QMessageBox:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText(
                    f"An error occurred while saving settings:\n{str(e)}")
                msg.exec_()
            print(f"Settings save error: {e}")

    def apply_theme_change(self, new_theme):
        """Apply theme change to the application"""
        try:
            self.view.theme.set_theme(new_theme)

            # Refresh the settings page styling for the new theme
            self.view.config_view.refresh_styling()

            # Update the theme button icon
            from PyQt5 import QtGui
            from utils.paths import get_icon_path
            self.view.sidebar.theme_btn.setIcon(QtGui.QIcon(
                get_icon_path().get("base") + f'{"dark" if new_theme == "light" else "light"}.svg'))
        except (ImportError, AttributeError, FileNotFoundError) as e:
            print(f"Error applying theme change: {e}")

    def reset_settings_to_defaults(self):
        """Reset settings to default values"""
        default_settings = {
            "theme": "light",
            "media_output_path": "/output",
            "report": "/reports",
            "recursive_folder_search": False,
            "threshold": 0.7
        }
        self.model.save_settings(default_settings)
        self.load_settings_to_ui()
