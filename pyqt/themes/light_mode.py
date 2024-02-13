from PyQt5.QtWidgets import QWidget

from utils.paths import get_css_path
from utils.styles import load_css


class Light(QWidget):
    def __init__(self, view_instance):
        super().__init__()
        self.view_instance = view_instance
        self.window = view_instance.window

    def apply(self):
        load_css(self.window, get_css_path().get("light"))
