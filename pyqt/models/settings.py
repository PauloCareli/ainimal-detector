
class SettingModel:
    def __init__(self):
        # Add configuration-related properties and methods as needed
        self.theme = "light"
        self.media_output_path = "output"
        self.report_output_path = "reports"
        self.recursive_folder_search = False
        self.threshold = 0.7

    def set_general_settings(self, json_file):
        self.theme = json_file.get("theme", self.theme)
        self.media_output_path = json_file.get(
            "media_output_path", self.media_output_path)
        self.report_output_path = json_file.get(
            "report_output_path", json_file.get("report", self.report_output_path))  # Backward compatibility
        self.recursive_folder_search = json_file.get(
            "recursive_folder_search", self.recursive_folder_search)
        self.threshold = json_file.get("threshold", self.threshold)

    def get_all_settings(self):
        """Get all current settings as a dictionary"""
        return {
            "theme": self.theme,
            "media_output_path": self.media_output_path,
            "report_output_path": self.report_output_path,
            "recursive_folder_search": self.recursive_folder_search,
            "threshold": self.threshold
        }

    def update_settings(self, settings_dict):
        """Update settings from a dictionary"""
        for key, value in settings_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
