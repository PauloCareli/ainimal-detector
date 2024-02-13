from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle("AInimal detection")
        self.setGeometry(100, 100, 800, 600)
