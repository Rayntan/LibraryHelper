import sys
from PyQt5.QtWidgets import QAction

from ui.design import *
from config import Config
from page_controllers.connection_controller import ConnectionController
from page_controllers.author_controller import AuthorController
from page_controllers.book_controller import BookController
from page_controllers.user_controller import UserController
from page_controllers.genre_controller import GenreController
from page_controllers.report_controller import ReportController
from page_controllers.take_return_controller import TakeReturnController


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

        self.config = Config()

        self.user_controller = UserController(self, self.ui)
        self.genre_controller = GenreController(self, self.ui)
        self.author_controller = AuthorController(self, self.ui)
        self.book_controller = BookController(self, self.ui)
        self.take_return_controller = TakeReturnController(self, self.ui)
        self.report_controller = ReportController(self, self.ui, self.config)
        self.connection_controller = ConnectionController(self, self.ui, self.config)

    @property
    def conn(self):
        return self.connection_controller.get_connection()

    def closeEvent(self, event):
        self.connection_controller.close_connection()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_app = MyWin()
    my_app.show()
    sys.exit(app.exec_())
