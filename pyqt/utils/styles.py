def load_css(self, path):
    with open(path, 'r') as file:
        style_sheet = file.read()
        # self.window.setStyleSheet(style_sheet)
        self.setStyleSheet(style_sheet)
