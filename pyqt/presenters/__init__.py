

from .image import ImagePresenter


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self

        self.image_presenter = ImagePresenter(model, view)

    def delegate_to_presenter(self, presenter, method_name, *args, **kwargs):
        # Generic method to delegate a call to a specific presenter and method
        if hasattr(presenter, method_name):
            method = getattr(presenter, method_name)
            return method(*args, **kwargs)
        else:
            raise AttributeError(
                f"{presenter.__class__.__name__} has no method {method_name}")

    def on_folder_selected(self, folder_path):
        print('chegou aqui 1')
        self.delegate_to_presenter(
            self.image_presenter, 'on_folder_selected', folder_path)

    def load_folder_contents(self, folder_path):
        self.delegate_to_presenter(
            self.image_presenter, 'load_folder_contents', folder_path)

    def get_video_frame(self, file_path):
        self.delegate_to_presenter(
            self.image_presenter, 'get_video_frame', file_path)
