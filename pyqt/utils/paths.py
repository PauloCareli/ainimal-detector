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
        "menu": base + "menu.png",
        "home": base + "home.png",
        "predict": base + "predict.png",
        "report": base + "report.png",
        "image": base + "image.png",
        "settings": base + "settings.svg",
        "about": base + "about.png",
        "taskbar": base + "taskbar.png"
    }


def get_image_path():
    base = "pyqt/assets/images/"

    return {
        "base": base,
        "welcome": base + "welcome.png"
    }
