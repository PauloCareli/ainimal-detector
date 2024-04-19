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
                threshold=model_data.get('threshold', 0.6)
            )
            ai_models.append(ai_model)

        return ai_models

    def load_ai_models(self):
        json_file_path = 'pyqt/ai_models.json'  # Path to your JSON file
        data = load_json(json_file_path)

        return self.create_ai_models_from_data(data)

    def load_settings(self, settings={}):
        json_file_path = "pyqt/settings.json"
        settings = load_json(json_file_path)
        self.settings_model.set_general_settings(settings)
        print("Settings loaded")
    # def save_settings(self, settings={}):
    #     if len(settings):
    #         for key, value in settings.items():
    #             self.settings_model.get(key) = value
