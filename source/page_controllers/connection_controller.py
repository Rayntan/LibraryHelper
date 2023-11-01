from db import get_connection
from psycopg2 import OperationalError
from PyQt5.QtWidgets import QMessageBox


class ConnectionController:
    """
    Контроллер страницы для работы с подключением к БД в приложении
    """
    def __init__(self, application, ui, config):
        self.application = application
        self.ui = ui
        self.config = config
        self.conn = None
        self.bind_methods()
        self.update_connection_settings()

    def bind_methods(self):
        self.ui.saveDBConnectionData.clicked.connect(self.save_connect_data)

    def get_connection(self):
        if not self.conn:
            self.connect_to_db()
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def connect_to_db(self):
        try:
            self.conn = get_connection(self.config.db_data)
        except OperationalError:
            QMessageBox.critical(
                self.application, "Ошибка соединения",
                "Укажите верные данные для подключения к базе данных", QMessageBox.Ok
            )
            raise ConnectionError

    def update_connection_settings(self):
        self.ui.hostLineEdit.setText(self.config.db_data["host"])
        self.ui.portLineEdit.setText(self.config.db_data["port"])
        self.ui.userLineEdit.setText(self.config.db_data["user"])
        self.ui.passwordLineEdit.setText(self.config.db_data["password"])
        self.ui.dbNameLineEdit.setText(self.config.db_data["dbname"])

    def save_connect_data(self):
        self.config.db_data = {
            "host": self.ui.hostLineEdit.text(),
            "port": self.ui.portLineEdit.text(),
            "user": self.ui.userLineEdit.text(),
            "password": self.ui.passwordLineEdit.text(),
            "dbname": self.ui.dbNameLineEdit.text()
        }
        QMessageBox.information(
            self.application, 'Данные о подключении успешно сохранены',
            'Данные о подключении успешно сохранены', QMessageBox.Ok
        )
        try:
            self.connect_to_db()
            QMessageBox.information(
                self.application, 'Подключение восстановлено',
                'Подключение восстановлено', QMessageBox.Ok
            )
        except ConnectionError:
            QMessageBox.critical(
                self.application, "Ошибка соединения",
                "Укажите верные данные для подключения к базе данных", QMessageBox.Ok
            )
