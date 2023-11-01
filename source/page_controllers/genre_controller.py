from PyQt5.QtWidgets import QMessageBox

from services.genre_service import GenreService, InGenre
from services.exceptions import UniqueException


class GenreController:
    """
    Контроллер страницы для работы с жанрами в приложении
    """
    def __init__(self, application, ui):
        self.application = application
        self.ui = ui
        self.bind_methods()

        self.genres = []
        self.current_genre = None
        self.is_new_genre_mode = None
        self.start_new_mode()

    def start_new_mode(self):
        self.is_new_genre_mode = True
        self.ui.deleteGenreBtn.setEnabled(False)

    def start_edit_mode(self):
        self.is_new_genre_mode = False
        self.ui.deleteGenreBtn.setEnabled(True)

    def bind_methods(self):
        self.ui.clearGenreSearchFieldBtn.clicked.connect(self.clear_search_genre_fields)
        self.ui.searchGenreBtn.clicked.connect(self.search_genre)
        self.ui.editSelectedGenreBtn.clicked.connect(self.edit_genre)
        self.ui.deleteGenreBtn.clicked.connect(self.delete_genre)
        self.ui.createNewGenreBtn.clicked.connect(self.create_new_genre)
        self.ui.saveGenreBtn.clicked.connect(self.save_genre)

    def clear_search_genre_fields(self):
        self.ui.searchGenreLineEdit.setText("")

    def search_genre(self):
        try:
            genre_service = GenreService(self.application.conn)
            self.genres = genre_service.get_list_by_search_conditions(
                name=self.ui.searchGenreLineEdit.text()
            )
            self.update_genre_list()
        except ConnectionError:
            return

    def update_genre_list(self):
        self.ui.genreList.clear()
        self.ui.genreList.addItems(
            [f"{genre.name} ({genre.id})" for genre in self.genres]
        )

    def clear_genre_form(self):
        self.ui.genreLineEdit.setText("")
        self.current_genre = None

    def create_new_genre(self):
        self.start_new_mode()
        self.clear_genre_form()

    def edit_genre(self):
        if not self.ui.genreList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Жанр не выбран", QMessageBox.Ok
            )
            return
        self.start_edit_mode()
        index = self.ui.genreList.currentRow()
        self.current_genre = self.genres[index]
        self.ui.genreLineEdit.setText(self.current_genre.name)

    def delete_genre(self):
        try:
            genre_service = GenreService(self.application.conn)
            genre_service.delete(self.current_genre.id)
            self.genres = list(filter(lambda genre: genre.id != self.current_genre.id, self.genres))
            self.update_genre_list()
            self.current_genre = None
            self.clear_genre_form()
            QMessageBox.information(
                self.application, "Удаление завершено", "Жанр успешно удален", QMessageBox.Ok
            )
        except ConnectionError:
            return

    def save_genre(self):
        new_name = self.ui.genreLineEdit.text()
        try:
            genre_service = GenreService(self.application.conn)
            if self.is_new_genre_mode:
                self.save_new_genre(genre_service, new_name)
            else:
                self.save_updated_genre(genre_service, new_name)
        except ConnectionError:
            return

    def save_new_genre(self, genre_service, new_name):
        genre = InGenre(
            name=new_name
        )
        try:
            genre_service.create(genre)
        except UniqueException:
            QMessageBox.critical(
                self.application, "Ошибка", "Жанр с таким названием уже существует", QMessageBox.Ok
            )
            return
        self.clear_genre_form()
        QMessageBox.information(
            self.application, "Создание завершено", "Жанр успешно создан", QMessageBox.Ok
        )

    def save_updated_genre(self, genre_service, new_name):
        self.current_genre.name = new_name
        try:
            genre_service.update(self.current_genre)
        except UniqueException:
            QMessageBox.critical(
                self.application, "Ошибка", "Жанр с таким названием уже существует", QMessageBox.Ok
            )
            return
        for (index, genre) in enumerate(self.genres):
            if genre.id == self.current_genre.id:
                self.genres[index] = self.current_genre
                break
        self.update_genre_list()

        self.clear_genre_form()
        self.current_genre = None
        self.start_new_mode()
        QMessageBox.information(
            self.application, "Редактирование завершено", "Данные о жанре успешно сохранены", QMessageBox.Ok
        )
