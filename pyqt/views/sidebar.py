from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QWidget
from PyQt5.QtCore import Qt

from utils.paths import get_css_path, get_icon_path
from utils.styles import load_css

ICON_SIZE = 30


class Sidebar(QWidget):
    def __init__(self, view_instance):
        super().__init__()
        self.view = view_instance
        self.window = view_instance.window

        # add all widgets
        self.theme_btn = QtWidgets.QToolButton(self)
        self.theme_btn.setMinimumHeight(ICON_SIZE)
        self.btn_0 = QPushButton('Home', self)
        self.btn_1 = QPushButton('Predict', self)
        self.btn_2 = QPushButton('Report', self)
        self.btn_3 = QPushButton('Image', self)
        self.btn_4 = QPushButton('Settings', self)

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
        left_layout_top = QVBoxLayout()
        left_layout_middle = QVBoxLayout()
        left_layout_bottom = QVBoxLayout()
        left_layout_top.addWidget(self.theme_btn, alignment=Qt.AlignCenter)
        left_layout_middle.addWidget(self.btn_0)
        left_layout_middle.addWidget(self.btn_1)
        left_layout_middle.addWidget(self.btn_2)
        left_layout_middle.addWidget(self.btn_3)
        left_layout_bottom.addWidget(self.btn_4)
        left_layout_middle.addStretch(5)
        left_layout_middle.setSpacing(20)
        left_layout.addLayout(left_layout_top)
        left_layout.addLayout(left_layout_middle)
        left_layout.addLayout(left_layout_bottom)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)

        left_layout.setStretch(0, 10)
        left_layout.setStretch(1, 80)
        left_layout.setStretch(2, 10)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab0, '')
        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        load_css(left_widget, get_css_path().get("sidebar"))
        load_css(self.right_widget, get_css_path().get("sidebar"))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.view.title_bar)
        # main_layout.setContentsMargins(0, 0, 0, 0)
        # main_layout.setSpacing(0)

        secondary_layout = QHBoxLayout()
        secondary_layout.addWidget(left_widget)
        secondary_layout.addWidget(self.right_widget)
        secondary_layout.setContentsMargins(5, 5, 5, 5)
        secondary_layout.setSpacing(0)

        secondary_layout.setStretch(0, 40)
        secondary_layout.setStretch(1, 200)
        main_layout.addLayout(secondary_layout)
        # main_layout.addWidget(left_widget)
        # main_layout.addWidget(self.right_widget)
        # main_layout.setStretch(0, 40)
        # main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        # self.window.addWidget(main_widget)

        # vbox = QtWidgets.QVBoxLayout(self)
        # vbox.addWidget(self)
        # vbox.setContentsMargins(0, 0, 0, 0)
        # vbox.setSpacing(0)
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.m_content)
        # layout.setContentsMargins(5, 5, 5, 5)
        # layout.setSpacing(0)
        # vbox.addLayout(layout)

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
        self.theme_btn.setIcon(QtGui.QIcon(
            get_icon_path().get("base") + f'{self.view.presenter.model.config_model.theme}.svg'))
        if self.view.presenter.model.config_model.theme == "light":
            self.view.presenter.model.config_model.theme = "dark"
        else:
            self.view.presenter.model.config_model.theme = "light"
        self.view.theme.set_theme(
            self.view.presenter.model.config_model.theme)
        return

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
