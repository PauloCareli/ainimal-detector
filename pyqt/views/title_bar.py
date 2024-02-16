from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from utils.paths import get_css_path
from utils.styles import load_css

ICON_SIZE = 20


class TitleBar(QWidget):
    def __init__(self, view_instance):
        super().__init__()
        self.window = view_instance.window

        load_css(self, get_css_path().get("titleBar"))

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.minimize = QtWidgets.QToolButton(self)
        self.minimize.setIcon(QtGui.QIcon('pyqt/icons/Minus.svg'))
        self.maximize = QtWidgets.QToolButton(self)
        self.maximize.setIcon(QtGui.QIcon('pyqt/icons/MaximizeWindow.svg'))
        close = QtWidgets.QToolButton(self)
        close.setIcon(QtGui.QIcon('pyqt/icons/Close.svg'))

        self.minimize.setMinimumHeight(ICON_SIZE)
        close.setMinimumHeight(ICON_SIZE)
        self.maximize.setMinimumHeight(ICON_SIZE)
        label = QtWidgets.QLabel(self)
        label.setText("AInimal Detector")
        self.setWindowTitle("AInimal Detector")
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1, 500)
        hbox.setSpacing(3)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Fixed)
        self.maxNormal = False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        self.window.showMinimized()

    def showMaxRestore(self):
        if self.maxNormal:
            self.window.showNormal()
            self.maxNormal = False
            self.maximize.setIcon(QtGui.QIcon('pyqt/icons/MaximizeWindow.svg'))
        else:
            self.window.showMaximized()
            self.maxNormal = True
            self.maximize.setIcon(QtGui.QIcon('pyqt/icons/MinimizeWindow.svg'))

    def close(self):
        self.window.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.window.moving = True
            self.window.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.window.moving:
            self.window.move(event.globalPos() - self.window.offset)

    def mouseReleaseEvent(self, event):
        self.window.moving = False

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.showMaxRestore()
