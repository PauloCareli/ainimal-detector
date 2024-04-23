
class SettingModel:
    def __init__(self):
        # Add configuration-related properties and methods as needed
        self.theme = "light"
        self.media_output_path = "/output"
        self.report = "pyqt/reports"
        self.recursive_folder_search = False

    def set_general_settings(self, json_file):
        self.theme = json_file.get("theme", self.theme)
        self.media_output_path = json_file.get(
            "media_output_path", self.media_output_path)
        self.report = json_file.get("report", self.report)
        self.recursive_folder_search = json_file.get(
            "recursive_folder_search", self.recursive_folder_search)
