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
        self.btn_5 = QPushButton('About', self)

        # First Box
        self.theme_btn.clicked.connect(self.theme)

        # Second box
        self.btn_0.clicked.connect(lambda: self.on_button_click(self.btn_0, 0))
        self.btn_1.clicked.connect(lambda: self.on_button_click(self.btn_1, 1))
        self.btn_2.clicked.connect(lambda: self.on_button_click(self.btn_2, 2))
        self.btn_3.clicked.connect(lambda: self.on_button_click(self.btn_3, 3))

        # Third box
        self.btn_4.clicked.connect(lambda: self.on_button_click(self.btn_4, 4))
        self.btn_5.clicked.connect(lambda: self.on_button_click(self.btn_5, 5))

        # add tabs
        self.tab0 = self.home()
        self.tab1 = self.predict()
        self.tab2 = self.report()
        self.tab3 = self.ui_image()
        self.tab4 = self.ui_config()
        self.tab5 = self.about()

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
        left_layout_bottom.addWidget(self.btn_5)
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
        self.right_widget.addTab(self.tab5, '')

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

    # --------------------------------------------------------------------- #

    def on_button_click(self, button, index):
        self.right_widget.setCurrentIndex(index)
        self.highlight_button(button)

    def highlight_button(self, button):
        # Reset the stylesheet for all buttons
        for btn in [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5]:
            btn.setStyleSheet('')

        # Highlight it
        button.setStyleSheet('background-color: #00ccff;;')

    # --------------------------------------------------------------------- #
    # Pages

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

    def about(self):
        return self.view.about_view
