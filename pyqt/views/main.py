from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setMinimumSize(960, 600)
        self.edge_thickness = 10
        self.pressing = False
        self.curPos = None

    def mousePressEvent(self, event):
        self.pressing = True
        self.curPos = self.mapFromGlobal(QtGui.QCursor.pos())

    def mouseMoveEvent(self, event):
        if self.pressing and event.buttons() == Qt.LeftButton:
            # Resizing the window according to which edge is dragged
            global_cursor_pos = QtGui.QCursor.pos()
            rect = self.geometry()

            # Top-Left corner
            if self.curPos.x() <= self.edge_thickness and self.curPos.y() <= self.edge_thickness:
                dx = global_cursor_pos.x() - rect.left()
                dy = global_cursor_pos.y() - rect.top()
                self.setGeometry(global_cursor_pos.x(), global_cursor_pos.y(
                ), rect.width() - dx, rect.height() - dy)

            # Bottom-Right corner
            elif self.curPos.x() >= rect.width() - self.edge_thickness and self.curPos.y() >= rect.height() - self.edge_thickness:
                self.resize(global_cursor_pos.x() - rect.left(),
                            global_cursor_pos.y() - rect.top())

            # Remaining Corners
            elif self.curPos.x() <= self.edge_thickness:  # Left edge
                dx = global_cursor_pos.x() - rect.left()
                self.setGeometry(global_cursor_pos.x(), rect.top(),
                                 rect.width() - dx, rect.height())
            elif self.curPos.y() <= self.edge_thickness:  # Top edge
                dy = global_cursor_pos.y() - rect.top()
                self.setGeometry(rect.left(), global_cursor_pos.y(),
                                 rect.width(), rect.height() - dy)
            elif self.curPos.x() >= rect.width() - self.edge_thickness:  # Right edge
                self.resize(global_cursor_pos.x() - rect.left(), rect.height())
            elif self.curPos.y() >= rect.height() - self.edge_thickness:  # Bottom edge
                self.resize(rect.width(), global_cursor_pos.y() - rect.top())

            self.curPos = self.mapFromGlobal(QtGui.QCursor.pos())

        # Update cursor icon based on position
        pos = event.pos()
        if pos.x() < self.edge_thickness or pos.x() > self.width() - self.edge_thickness:
            self.setCursor(QtGui.QCursor(Qt.SizeHorCursor))
        elif pos.y() < self.edge_thickness or pos.y() > self.height() - self.edge_thickness:
            self.setCursor(QtGui.QCursor(Qt.SizeVerCursor))
        else:
            self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        self.pressing = False
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))
