from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

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

        # Add the three-line menu button
        self.menu_btn = QtWidgets.QToolButton(self)
        self.menu_btn.setIcon(QIcon(get_icon_path().get("menu")))
        self.menu_btn.clicked.connect(self.toggle_menu)
        self.menu_visible = True

        self.btn_0 = QPushButton(
            QIcon(get_icon_path().get("home")), 'Home', self)
        self.btn_1 = QPushButton(
            QIcon(get_icon_path().get("predict")), 'Predict', self)
        self.btn_2 = QPushButton(
            QIcon(get_icon_path().get("report")), 'Report', self)
        self.btn_3 = QPushButton(
            QIcon(get_icon_path().get("image")), 'Image', self)
        self.btn_4 = QPushButton(
            QIcon(get_icon_path().get("settings")), 'Settings', self)
        self.btn_5 = QPushButton(
            QIcon(get_icon_path().get("about")), 'About', self)

        # First Box
        self.theme_btn.clicked.connect(self.theme)

        # Second box
        self.btn_0.clicked.connect(lambda: self.on_button_click(self.btn_0, 0))
        self.btn_1.clicked.connect(lambda: self.on_button_click(self.btn_1, 1))
        self.btn_1.clicked.connect(lambda: self.load_models())
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
        left_layout_top.addWidget(self.menu_btn, alignment=Qt.AlignCenter)
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

        secondary_layout = QHBoxLayout()
        secondary_layout.addWidget(left_widget)
        secondary_layout.addWidget(self.right_widget)
        secondary_layout.setContentsMargins(5, 5, 5, 5)
        secondary_layout.setSpacing(0)

        secondary_layout.setStretch(0, 40)
        secondary_layout.setStretch(1, 200)
        self.secondary_layout = secondary_layout
        main_layout.addLayout(secondary_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.window.setCentralWidget(main_widget)

        self.highlight_button(self.btn_0)

    def load_models(self):
        if "presenter" in dir(self.view):
            attributes_and_methods = dir(self.view)
            print(attributes_and_methods)
            # self.ai_models = self.model.load_ai_models()
            print(dir(self.view.presenter))
            self.ai_models = self.view.presenter.load_ai_models()

    # --------------------------------------------------------------------- #
    # Sidebar Methods

    def on_button_click(self, button, index):
        self.right_widget.setCurrentIndex(index)
        self.highlight_button(button)

    def highlight_button(self, button):
        # Reset the stylesheet for all buttons
        for btn in [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5]:
            btn.setStyleSheet('')

        style = 'padding: 5px;' if not self.menu_visible else 'padding: 10px 20px;'
        # Highlight it
        self.set_button_style(
            'padding: 5px;' if not self.menu_visible else 'padding: 10px 20px;')
        button.setStyleSheet(f'background-color: #00ccff;{style};')

    def get_buttons(self):
        return [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5]

    def hide_buttons(self):
        # Hide only the text labels of the buttons
        for btn, label in [(self.btn_0, "Home"), (self.btn_1, "Predict"), (self.btn_2, "Report"),
                           (self.btn_3, "Image"), (self.btn_4, "Settings"), (self.btn_5, "About")]:
            original_text = btn.text()  # Store the original text
            btn.setProperty("original_text", original_text)
            btn.setText("")
            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter)
        self.update_sidebar_size()

    def show_buttons(self):
        # Show the text labels of the buttons
        for btn in self.get_buttons():
            original_text = btn.property("original_text")
            if original_text:
                btn.setText(original_text)

        self.update_sidebar_size()

    def toggle_menu(self):
        if self.menu_visible:
            self.hide_buttons()
        else:
            self.show_buttons()

        # Toggle the menu visibility state
        self.menu_visible = not self.menu_visible

    def update_sidebar_size(self):
        self.secondary_layout.setStretch(0, 2)
        self.set_button_style(
            'padding: 5px;' if self.menu_visible else 'padding: 10px 20px;')

    def set_button_style(self, style):
        # Apply the common style to all buttons
        for btn in self.get_buttons():
            btn.setStyleSheet(style)

    # --------------------------------------------------------------------- #
    # Pages

    def theme(self):
        self.theme_btn.setIcon(QIcon(
            get_icon_path().get("base") + f'{self.view.presenter.model.settings_model.theme}.svg'))
        if self.view.presenter.model.settings_model.theme == "light":
            self.view.presenter.model.settings_model.theme = "dark"
        else:
            self.view.presenter.model.settings_model.theme = "light"
        self.view.theme.set_theme(
            self.view.presenter.model.settings_model.theme)

        return

    def home(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Welcome to AInimal detector!'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)

        return main

    def predict(self):
        return self.view.predict

    def report(self):
        return self.view.csv_view

    def ui_image(self):
        return self.view.image_view

    def ui_config(self):
        return self.view.config_view

    def about(self):
        return self.view.about_view
