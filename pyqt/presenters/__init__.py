
from PyQt5 import QtGui
from utils.paths import get_icon_path

from .image import ImagePresenter
from .model import ModelPresenter
from .predict import PredictPresenter
from .settings import SettingsPresenter


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self

        self.image_presenter = ImagePresenter(model, view)
        self.model_presenter = ModelPresenter(model, view)
        self.predict_presenter = PredictPresenter(model, view)
        self.settings_presenter = SettingsPresenter(model, view)

        self.on_load_app()

    def on_load_app(self):
        current_theme = self.model.settings_model.theme
        self.view.sidebar.theme_btn.setIcon(QtGui.QIcon(
            get_icon_path().get("base") + f'{"dark" if current_theme == "light" else "dark"}.svg'))
        self.view.theme.set_theme(
            self.model.settings_model.theme)

        self.model.load_settings()

    def delegate_to_presenter(self, presenter, method_name, *args, **kwargs):
        # Generic method to delegate a call to a specific presenter and method
        if hasattr(presenter, method_name):
            method = getattr(presenter, method_name)
            return method(*args, **kwargs)
        else:
            raise AttributeError(
                f"{presenter.__class__.__name__} has no method {method_name}")

    def on_folder_selected(self, folder_path):
        self.delegate_to_presenter(
            self.image_presenter, 'on_folder_selected', folder_path)

    def load_folder_contents(self, folder_path):
        self.delegate_to_presenter(
            self.image_presenter, 'load_folder_contents', folder_path)

    def get_video_frame(self, file_path):
        self.delegate_to_presenter(
            self.image_presenter, 'get_video_frame', file_path)

    # Model
    def load_ai_models(self):
        self.delegate_to_presenter(
            self.model_presenter, 'load_ai_models')

    # Predict
    def predict(self, file_path, model):
        return self.delegate_to_presenter(
            self.predict_presenter, 'predict', file_path, model)
