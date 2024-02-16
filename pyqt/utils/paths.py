def get_css_path():
    base = "pyqt/styles/"

    return {
        "base": base,
        "image": base + 'image.css',
        "sidebar": base + 'sidebar.css',
        "dark": base + "dark_theme.css",
        "light": base + "light_theme.css",
        "titleBar": base + "title_bar.css"
    }


def get_icon_path():
    base = "pyqt/icons/"

    return {
        "base": base,
    }
