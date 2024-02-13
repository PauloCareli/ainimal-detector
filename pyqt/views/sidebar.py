from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget

from utils.paths import get_css_path
from utils.styles import load_css


class Sidebar(QWidget):
    def __init__(self, view_instance):
        super().__init__()
        self.view = view_instance
        self.window = view_instance.window

        # add all widgets
        self.theme_btn = QPushButton('Theme', self)
        self.btn_0 = QPushButton('Home', self)
        self.btn_1 = QPushButton('Predict', self)
        self.btn_2 = QPushButton('Report', self)
        self.btn_3 = QPushButton('Image', self)
        self.btn_4 = QPushButton('Config', self)

        self.theme_btn.clicked.connect(self.theme)
        self.btn_0.clicked.connect(self.button0)
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # add tabs
        self.tab0 = self.home()
        self.tab1 = self.predict()
        self.tab2 = self.report()
        self.tab3 = self.ui_image()
        self.tab4 = self.ui_config()

        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.theme_btn)
        left_layout.addWidget(self.btn_0)
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        load_css(left_widget, get_css_path().get("sidebar"))

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab0, '')
        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.window.setCentralWidget(main_widget)

    # -----------------
    # buttons

    def button0(self):
        self.right_widget.setCurrentIndex(0)

    def button1(self):
        self.right_widget.setCurrentIndex(1)

    def button2(self):
        self.right_widget.setCurrentIndex(2)

    def button3(self):
        self.right_widget.setCurrentIndex(3)

    def button4(self):
        self.right_widget.setCurrentIndex(4)

    # -----------------
    # pages

    def theme(self):
        if self.view.presenter.model.config_model.theme == "light":
            self.view.presenter.model.config_model.theme = "dark"
        else:
            self.view.presenter.model.config_model.theme = "light"
        print(self.view.presenter.model.config_model.theme)
        self.view.theme.set_theme(
            self.view.presenter.model.config_model.theme)
        return
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 0'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def home(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Home Page'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def predict(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 1'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def report(self):
        return self.view.csv_view

    def ui_image(self):
        return self.view.image_view

    def ui_config(self):
        return self.view.config_view
