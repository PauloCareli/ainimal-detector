from utils.json_manipulation import load_json
from .settings import SettingModel
from .image import ImageModel
from .ai_model import AIModel


class Model:
    def __init__(self):
        self.image_model = ImageModel()
        self.settings_model = SettingModel()
        self.ai_model = AIModel()

        self.on_load_app()

    def on_load_app(self):
        print('Models loaded')

    def create_ai_models_from_data(self, data):
        ai_models = []
        for model_data in data:
            ai_model = AIModel(
                name=model_data.get('name'),
                path=model_data.get('path'),
                description=model_data.get('description'),
                accuracy=model_data.get('accuracy', 0.0),
                threshold=model_data.get('threshold', 0.6),
                model_type=model_data.get('model_type'),
                version=model_data.get('version'),
                training_date=model_data.get('training_date'),
                map_50=model_data.get('map_50'),
                training_images=model_data.get('training_images'),
                classes=model_data.get('classes'),
                input_size=model_data.get('input_size'),
                supported_formats=model_data.get('supported_formats'),
                optimal_conditions=model_data.get('optimal_conditions'),
                training_dataset=model_data.get('training_dataset'),
                performance_notes=model_data.get('performance_notes')
            )
            ai_models.append(ai_model)

        return ai_models

    def load_ai_models(self):
        json_file_path = 'pyqt/ai_models.json'  # Path to your JSON file
        data = load_json(json_file_path)

        return self.create_ai_models_from_data(data)

    def load_settings(self, settings=None):
        if settings is None:
            settings = {}
        json_file_path = "pyqt/settings.json"
        settings = load_json(json_file_path)
        self.settings_model.set_general_settings(settings)
        print("Settings loaded")
        return self.settings_model.get_all_settings()

    def save_settings(self, settings=None):
        """Save settings to JSON file and update the model"""
        if settings is None:
            settings = {}
        if settings:
            # Update the settings model
            self.settings_model.update_settings(settings)

            # Save to JSON file
            json_file_path = "pyqt/settings.json"
            from utils.json_manipulation import save_json
            save_json(settings, path=json_file_path)
            print("Settings saved successfully")
            return True
        return False

    def get_current_settings(self):
        """Get current settings from the model"""
        return self.settings_model.get_all_settings()
