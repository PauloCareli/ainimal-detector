from utils.json_manipulation import load_ai_models_from_json
from .config import ConfigModel
from .image import ImageModel
from .ai_model import AIModel


class Model:
    def __init__(self):
        self.image_model = ImageModel()
        self.config_model = ConfigModel()
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
        data = load_ai_models_from_json(json_file_path)

        return self.create_ai_models_from_data(data)
