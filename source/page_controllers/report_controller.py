import os

from PyQt5.QtWidgets import QMessageBox
from reports.report_creator import ReportGenerator
from reports.report_data import *


class ReportController:
    """
    Контроллер страницы для работы с отчетами в приложении
    """
    def __init__(self, application, ui, config):
        self.application = application
        self.ui = ui
        self.config = config
        self.report_generator = ReportGenerator(self.config.report_dir_path)
        self.bind_methods()

    def bind_methods(self):
        self.ui.reportBtn1.clicked.connect(lambda: self._generate_report(**report_1))
        self.ui.reportBtn2.clicked.connect(lambda: self._generate_report(**report_2))
        self.ui.reportBtn3.clicked.connect(lambda: self._generate_report(**report_3))
        self.ui.reportBtn4.clicked.connect(lambda: self._generate_report(**report_4))
        self.ui.reportBtn5.clicked.connect(lambda: self._generate_report(**report_5))
        self.ui.reportBtn6.clicked.connect(lambda: self._generate_report(**report_6))
        self.ui.reportBtn7.clicked.connect(lambda: self._generate_report(**report_7))
        self.ui.reportBtn8.clicked.connect(lambda: self._generate_report(**report_8))

        self.ui.dirPathLineEdit.setText(self.config.report_dir_path)
        self.ui.saveDirPath.clicked.connect(self.save_dir_path)

    def _generate_report(self, title: str, query, headings_cells: list):
        if not os.path.exists(self.config.report_dir_path):
            QMessageBox.critical(
                self.application, "Ошибка ",
                "Укажите путь до директории для отчетов", QMessageBox.Ok
            )
            return
        try:
            with self.application.conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
            file_path = self.report_generator.generate_and_save(title, headings_cells, rows)
            QMessageBox.information(
                self.application, 'Отчет успешно создан',
                f'Отчет "{title}" находится по пути:\n {file_path}', QMessageBox.Ok
            )
        except ConnectionError:
            return

    def save_dir_path(self):
        new_dir_path = self.application.ui.dirPathLineEdit.text()
        self.report_generator = ReportGenerator(new_dir_path)
        self.config.report_dir_path = new_dir_path
        QMessageBox.information(
            self.application, 'Путь успешно сохранен',
            'Путь успешно сохранен', QMessageBox.Ok
        )
