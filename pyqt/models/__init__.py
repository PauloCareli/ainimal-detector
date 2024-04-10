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
