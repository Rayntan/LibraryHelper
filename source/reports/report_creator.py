import os

from fpdf import FPDF
from fpdf.fonts import FontFace
from os.path import join
from time import time


class ReportGenerator:
    """
    Генерирует отчет по переданным данным и сохраняет его по пути dir_path
    """
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    def generate_and_save(self, title: str, headings_cells: list, data_cells: list) -> str:
        report = Report()
        report.add_document_heading(title)
        report.add_table(headings_cells, data_cells)
        file_path = self._generate_file_path()
        report.output(file_path)
        return file_path

    def _generate_file_path(self) -> str:
        filename = f"{int(time())}.pdf"
        file_path = join(self.dir_path, filename)
        return file_path


class Report(FPDF):
    """
    Создает pdf-документ с заголовком и таблицей
    """
    def __init__(self):
        super().__init__()
        self.add_page()
        self.add_fonts()

    def add_fonts(self) -> None:
        self.add_font(family="Roboto", fname=os.path.join("fonts", "Roboto-Regular.ttf"))
        self.add_font(family="Roboto", style="B", fname=os.path.join("fonts", "Roboto-Bold.ttf"))
        self.set_font(family="Roboto", style="B", size=15)

    def add_document_heading(self, heading_text: str):
        self.text(10, 7, heading_text)

    def add_table(self, head_cells: list, data: list) -> None:
        table_headings_style = FontFace(emphasis="BOLD", color=255, fill_color=(128, 128, 128))
        with self.table(
                cell_fill_color=(224, 235, 255),
                headings_style=table_headings_style,
                line_height=6) as table:

            row = table.row()
            for head_cell in head_cells:
                row.cell(str(head_cell))

            self.set_font(family="Roboto", size=15)

            for data_row in data:
                row = table.row()
                for datum in data_row:
                    row.cell(str(datum))
