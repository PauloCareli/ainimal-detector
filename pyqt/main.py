import sys
from PyQt5.QtWidgets import QApplication

from models import Model
from views import View
from presenters import Presenter

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = Model()
    view = View()
    presenter = Presenter(model, view)

    view.window.show()
    sys.exit(app.exec_())
