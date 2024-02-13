from PyQt5.QtWidgets import QMainWindow


from .dark_mode import Dark
from .light_mode import Light


class Theme:
    def __init__(self, view_instance):
        self.dark = Dark(view_instance)
        self.light = Light(view_instance)

    def set_theme(self, theme):
        selected_theme = getattr(self, theme, None)

        if selected_theme:
            # Do something with the selected theme
            # For example, you might want to set it as the current theme
            selected_theme.apply()
            print(f"Theme set to {theme}")
        else:
            print(f"Theme {theme} not found")
        pass
