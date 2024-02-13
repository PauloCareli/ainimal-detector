

from .config import ConfigModel
from .image import ImageModel


class Model:
    def __init__(self):
        self.image_model = ImageModel()
        self.config_model = ConfigModel()
