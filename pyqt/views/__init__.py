from PyQt5.QtWidgets import QMainWindow


from .image import ImageView
from .config import ConfigView
from .main import MainWindow
from .sidebar import Sidebar
from .csv_viewer import CSVView
from themes import Theme


class View:
    def __init__(self):
        # self.window = QMainWindow()
        self.window = MainWindow()
        self.image_view = ImageView(self)
        self.config_view = ConfigView(self)
        self.csv_view = CSVView(self)

        self.theme = Theme(self)
        # Router
        self.sidebar = Sidebar(self)
