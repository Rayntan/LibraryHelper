from PyQt5.QtWidgets import QMessageBox

from services.author_service import AuthorService
from services.book_service import BookService, InBook
from services.exceptions import UniqueException
from services.genre_service import GenreService


class BookController:
    """
    Контроллер страницы для работы с книгами в приложении
    """
    def __init__(self, application, ui):
        self.application = application
        self.ui = ui
        self.bind_methods()

        self.books = []
        self.current_book = None
        self.current_book_genres = []
        self.old_book_genres = []
        self.current_book_authors = []
        self.old_book_authors = []

        self.search_genres = []
        self.search_authors = []

        self.is_new_book_mode = None
        self.start_new_mode()

    def start_new_mode(self):
        self.is_new_book_mode = True
        self.current_book_genres = []
        self.current_book_authors = []
        self.old_book_genres = []
        self.old_book_authors = []
        self.ui.deleteBookBtn.setEnabled(False)

    def start_edit_mode(self):
        self.is_new_book_mode = False
        self.ui.deleteBookBtn.setEnabled(True)

    def bind_methods(self):
        self.ui.clearBookSearchFieldBtn.clicked.connect(self.clear_search_book_fields)
        self.ui.searchBookBtn.clicked.connect(self.search_book)
        self.ui.editSelectedBookBtn.clicked.connect(self.edit_book)
        self.ui.deleteBookBtn.clicked.connect(self.delete_book)
        self.ui.createNewBookBtn.clicked.connect(self.create_new_book)
        self.ui.saveBookBtn.clicked.connect(self.save_book)
        self.ui.searchGenreBookBtn.clicked.connect(self.search_genre)
        self.ui.addSelectedGenreBookBtn.clicked.connect(self.add_genre)
        self.ui.deleteSelectedBookGenreBtn.clicked.connect(self.delete_genre)
        self.ui.searchAuthorBookBtn.clicked.connect(self.search_author)
        self.ui.addSelectedAuthorBookBtn.clicked.connect(self.add_author)
        self.ui.deleteSelectedBookAuthorBtn.clicked.connect(self.delete_author)

    def search_genre(self):
        try:
            genre_service = GenreService(self.application.conn)
            self.search_genres = genre_service.get_list_by_search_conditions(
                name=self.ui.searchGenreBookLineEdit.text()
            )
            self.update_search_genre_list()
        except ConnectionError:
            return

    def update_search_genre_list(self):
        self.ui.searchGenreBookList.clear()
        self.ui.searchGenreBookList.addItems(
            [f"{genre.name} ({genre.id})" for genre in self.search_genres]
        )

    def add_genre(self):
        if not self.ui.searchGenreBookList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Жанр не выбран", QMessageBox.Ok
            )
            return
        index = self.ui.searchGenreBookList.currentRow()
        search_genre = self.search_genres[index]
        if search_genre in self.current_book_genres:
            QMessageBox.critical(
                self.application, "Ошибка", "Книга уже принадлежит данному жанру", QMessageBox.Ok
            )
            return
        self.current_book_genres.append(search_genre)
        self.update_book_genre_list()

    def delete_genre(self):
        if not self.ui.genreBookList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Жанр не выбран", QMessageBox.Ok
            )
            return
        index = self.ui.genreBookList.currentRow()
        self.current_book_genres = self.current_book_genres[:index] + self.current_book_genres[index+1:]
        self.update_book_genre_list()

    def search_author(self):
        try:
            author_service = AuthorService(self.application.conn)
            self.search_authors = author_service.get_list_by_search_conditions(
                full_name=self.ui.searchAuthorBookLineEdit.text()
            )
            self.update_search_author_list()
        except ConnectionError:
            return

    def update_search_author_list(self):
        self.ui.searchAuthorBookList.clear()
        self.ui.searchAuthorBookList.addItems(
            [f"{author.full_name}" for author in self.search_authors]
        )

    def add_author(self):
        if not self.ui.searchAuthorBookList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Автор не выбран", QMessageBox.Ok
            )
            return
        index = self.ui.searchAuthorBookList.currentRow()
        search_author = self.search_authors[index]
        if search_author in self.current_book_authors:
            QMessageBox.critical(
                self.application, "Ошибка", "Книга уже принадлежит данному автору", QMessageBox.Ok
            )
            return
        self.current_book_authors.append(search_author)
        self.update_book_author_list()

    def delete_author(self):
        if not self.ui.authorBookList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Автор не выбран", QMessageBox.Ok
            )
            return
        index = self.ui.authorBookList.currentRow()
        self.current_book_authors = self.current_book_authors[:index] + self.current_book_authors[index+1:]
        self.update_book_author_list()

    def clear_search_book_fields(self):
        self.ui.searchBookLineEdit.setText("")

    def search_book(self):
        try:
            book_service = BookService(self.application.conn)
            self.books = book_service.get_list_by_search_conditions(
                name=self.ui.searchBookLineEdit.text()
            )
            self.update_book_list()
        except ConnectionError:
            return

    def update_book_list(self):
        self.ui.searchBookList.clear()
        self.ui.searchBookList.addItems(
            [f"{book.name} ({book.id})" for book in self.books]
        )

    def update_book_genre_list(self):
        self.ui.genreBookList.clear()
        self.ui.genreBookList.addItems(
            [f"{genre.name}" for genre in self.current_book_genres]
        )

    def update_book_author_list(self):
        self.ui.authorBookList.clear()
        self.ui.authorBookList.addItems(
            [f"{author.full_name}" for author in self.current_book_authors]
        )

    def clear_book_form(self):
        self.ui.BookLineEdit.setText("")
        self.ui.registerDateBookLabel.setText("")
        self.ui.bookPlace.setText("")
        self.current_book = None

        self.ui.searchGenreBookLineEdit.setText("")
        self.ui.searchAuthorBookLineEdit.setText("")

        self.ui.searchGenreBookList.clear()
        self.ui.searchAuthorBookList.clear()
        self.ui.genreBookList.clear()
        self.ui.authorBookList.clear()
        self.search_authors = []
        self.search_genres = []
        self.current_book_authors = []
        self.current_book_genres = []

    def create_new_book(self):
        self.start_new_mode()
        self.clear_book_form()

    def edit_book(self):
        if not self.ui.searchBookList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Книга не выбрана", QMessageBox.Ok
            )
            return
        self.start_edit_mode()
        index = self.ui.searchBookList.currentRow()
        self.current_book = self.books[index]
        try:
            book_service = BookService(self.application.conn)
            self.ui.bookPlace.setText(book_service.get_book_place(self.current_book.id))
            self.current_book_genres = book_service.get_genres(self.current_book.id)
            self.current_book_authors = book_service.get_authors(self.current_book.id)
            self.old_book_genres = [bg for bg in self.current_book_genres]
            self.old_book_authors = [ba for ba in self.current_book_authors]

            self.ui.BookLineEdit.setText(self.current_book.name)
            self.ui.registerDateBookLabel.setText(str(self.current_book.register_date))
            self.update_book_genre_list()
            self.update_book_author_list()
        except ConnectionError:
            return

    def delete_book(self):
        try:
            book_service = BookService(self.application.conn)
            book_service.delete(self.current_book.id)
            self.books = list(filter(lambda book: book.id != self.current_book.id, self.books))
            self.update_book_list()
            self.current_book = None
            self.clear_book_form()
            QMessageBox.information(
                self.application, "Удаление завершено", "Книга успешно удалена", QMessageBox.Ok
            )
        except ConnectionError:
            return

    def save_book(self):
        new_name = self.ui.BookLineEdit.text()
        try:
            book_service = BookService(self.application.conn)
            if self.is_new_book_mode:
                self.save_new_book(book_service, new_name)
            else:
                self.save_updated_book(book_service, new_name)
        except ConnectionError:
            return

    def save_new_book(self, book_service, new_name):
        try:
            book = book_service.create(InBook(name=new_name))
        except UniqueException:
            QMessageBox.critical(
                self.application, "Ошибка", "Книга с таким названием уже существует", QMessageBox.Ok
            )
            return
        for genre in self.current_book_genres:
            book_service.add_genre(book.id, genre.id)
        for author in self.current_book_authors:
            book_service.add_author(book.id, author.id)
        self.clear_book_form()
        QMessageBox.information(
            self.application, "Создание завершено", "Книга успешно создана", QMessageBox.Ok
        )

    def save_updated_book(self, book_service, new_name):
        self.current_book.name = new_name
        try:
            book_service.update(self.current_book)
        except UniqueException:
            QMessageBox.critical(
                self.application, "Ошибка", "Книга с таким названием уже существует", QMessageBox.Ok
            )
            return
        for author in self.current_book_authors:
            if author not in self.old_book_authors:
                book_service.add_author(self.current_book.id, author.id)
        for author in self.old_book_authors:
            if author not in self.current_book_authors:
                book_service.remove_author(self.current_book.id, author.id)
        for genre in self.current_book_genres:
            if genre not in self.old_book_genres:
                book_service.add_genre(self.current_book.id, genre.id)
        for genre in self.old_book_genres:
            if genre not in self.current_book_genres:
                book_service.remove_genre(self.current_book.id, genre.id)

        for (index, book) in enumerate(self.books):
            if book.id == self.current_book.id:
                self.books[index] = self.current_book
                break
        self.update_book_list()

        self.clear_book_form()
        self.current_book = None
        self.start_new_mode()
        QMessageBox.information(
            self.application, "Редактирование завершено", "Данные о книге успешно сохранены", QMessageBox.Ok
        )
