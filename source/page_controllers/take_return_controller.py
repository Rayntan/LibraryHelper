import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox
from services.book_service import BookService
from services.user_service import UserService
from services.user_book_service import UserBookService, InUserBook


class TakeReturnController:
    """
    Контроллер страницы для работы с фактами взятия/возвращения в приложении
    """
    def __init__(self, application, ui):
        self.application = application
        self.ui = ui

        self.search_users = []
        self.current_user = None
        self.search_books = []
        self.books = []

        self.set_default_expected_return_date()
        self.bind_methods()

    @property
    def is_take_fact(self):
        return self.ui.factTakeRadioBtn.isChecked()

    def set_default_expected_return_date(self):
        self.ui.expectedReturnDate.setDate(QDate.currentDate().addDays(14))

    def bind_methods(self):
        self.ui.factSearchUserBtn.clicked.connect(self.search_user)
        self.ui.factAddSelectedUserBtn.clicked.connect(self.add_selected_user)
        self.ui.factClearFieldsBtn.clicked.connect(self.clear_fact_fields)
        self.ui.factSearchBookBtn.clicked.connect(self.search_book)
        self.ui.factTakeRadioBtn.toggled.connect(self.clear_books)
        self.ui.factReturnRadioBtn.toggled.connect(self.clear_books)
        self.ui.factAddSelectedBookBtn.clicked.connect(self.add_book)
        self.ui.factDeleteSelectedBookBtn.clicked.connect(self.delete_selected_book)
        self.ui.newFactBtn.clicked.connect(self.create_new_fact)

    def search_user(self):
        try:
            user_service = UserService(self.application.conn)
            self.search_users = user_service.get_list_by_search_conditions(
                firstname=self.ui.searchFirstnameLineEdit.text(),
                lastname=self.ui.factLastnameLineEdit.text(),
                middlename=self.ui.searchMiddlenameLineEdit.text(),
            )
            self.update_user_list()
        except ConnectionError:
            return

    def update_user_list(self):
        self.ui.factSearchUserList.clear()
        self.ui.factSearchUserList.addItems(
            [f"{user.lastname} {user.firstname} {user.middlename} ({user.id})" for user in self.search_users]
        )

    def add_selected_user(self):
        if not self.ui.factSearchUserList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Пользователь не выбран", QMessageBox.Ok
            )
            return
        index = self.ui.factSearchUserList.currentRow()
        self.set_current_user(self.search_users[index])

    def set_current_user(self, new_current_user):
        self.clear_fact_fields()
        self.current_user = new_current_user
        self.ui.factUserLabel.setText(
            f"{self.current_user.lastname} {self.current_user.firstname} {self.current_user.middlename}"
        )

    def clear_fact_fields(self):
        self.current_user = None
        self.ui.factUserLabel.setText("Не выбран")
        self.ui.factTakeRadioBtn.setChecked(True)
        self.set_default_expected_return_date()
        self.books = []
        self.clear_books()

    def clear_books(self):
        self.books = []
        self.ui.factBookList.clear()
        self.search_books = []
        self.ui.factSearchBookList.clear()

    def search_book(self):
        if not self.current_user:
            QMessageBox.critical(
                self.application, "Ошибка", "Пользователь не выбран", QMessageBox.Ok
            )
            return
        try:
            book_service = BookService(self.application.conn)
            if self.is_take_fact:
                self.search_books = book_service.get_free_books()
            else:
                self.search_books = book_service.get_books_on_user_hands(self.current_user.id)
            self.update_search_book_list()
        except ConnectionError:
            return

    def update_search_book_list(self):
        self.ui.factSearchBookList.clear()
        self.ui.factSearchBookList.addItems(
            [f"{book.name}" for book in self.search_books]
        )

    def add_book(self):
        if not self.ui.factSearchBookList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Книга не выбрана", QMessageBox.Ok
            )
            return
        index = self.ui.factSearchBookList.currentRow()
        book = self.search_books[index]
        if book in self.books:
            QMessageBox.warning(
                self.application, "Предупреждение",
                "Данная книга уже есть в списке для создания факта взятия/возвращения", QMessageBox.Ok
            )
            return
        self.books.append(book)
        self.update_book_list()

    def update_book_list(self):
        self.ui.factBookList.clear()
        self.ui.factBookList.addItems(
            [f"{book.name}" for book in self.books]
        )

    def delete_selected_book(self):
        if not self.ui.factBookList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Книга не выбрана", QMessageBox.Ok
            )
            return
        index = self.ui.factBookList.currentRow()
        self.books = self.books[:index] + self.books[index+1:]
        self.update_book_list()

    def create_new_fact(self):
        if not self.current_user:
            QMessageBox.critical(
                self.application, "Ошибка", "Не выбран пользователь", QMessageBox.Ok
            )
            return
        if not self.books:
            QMessageBox.critical(
                self.application, "Ошибка", "Не выбраны книги", QMessageBox.Ok
            )
            return
        try:
            user_book_service = UserBookService(self.application.conn)
            if self.is_take_fact:
                self.save_take_fact(user_book_service)
            else:
                self.save_return_fact(user_book_service)
            self.clear_fact_fields()
        except ConnectionError:
            return

    def save_take_fact(self, user_book_service):
        if self.ui.expectedReturnDate.date() <= QDate.currentDate():
            QMessageBox.critical(
                self.application, "Ошибка", "Дата возвращения должна быть позже сегодняшней даты", QMessageBox.Ok
            )
            return
        expected_return_date = self.ui.expectedReturnDate.date().toPyDate()
        for book in self.books:
            user_book_service.create(
                InUserBook(user_id=self.current_user.id, book_id=book.id, expected_return_date=expected_return_date)
            )
        QMessageBox.information(
            self.application, "Создание завершено", "Факт выдачи успешно создан", QMessageBox.Ok
        )

    def save_return_fact(self, user_book_service):
        current_date = datetime.date.today()
        user_book_service.update_real_return_date(
            user_id=self.current_user.id, book_id_list=[book.id for book in self.books],
            real_return_date=current_date
        )
        QMessageBox.information(
            self.application, "Создание завершено", "Факт возвращения успешно создан", QMessageBox.Ok
        )
