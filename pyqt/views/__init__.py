from PyQt5.QtWidgets import QMainWindow


from .home import HomeView
from .image import ImageView
from .config import ConfigView
from .main import MainWindow
from .title_bar import TitleBar
from .sidebar import Sidebar
from .predict import PredictView
from .csv_viewer import CSVView
from .about import AboutView


from themes import Theme


class View:
    def __init__(self):
        # Main window
        self.window = MainWindow()

        # Title bar
        self.title_bar = TitleBar(self)

        # First box
        self.theme = Theme(self)

        # Second box
        self.home_view = HomeView(self)
        self.image_view = ImageView(self)
        self.predict = PredictView(self)
        self.csv_view = CSVView(self)

        # Third box
        self.config_view = ConfigView(self)
        self.about_view = AboutView(self)

        # Sidebar - Work as a Router
        self.sidebar = Sidebar(self)
