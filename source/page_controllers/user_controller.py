from PyQt5.QtWidgets import QMessageBox

from services.user_service import UserService, InUser


class UserController:
    """
    Контроллер страницы для работы с пользователями в приложении
    """
    def __init__(self, application, ui):
        self.application = application
        self.ui = ui
        self.bind_methods()

        self.users = []
        self.current_user = None
        self.is_new_user_mode = None
        self.start_new_mode()

    def start_new_mode(self):
        self.is_new_user_mode = True
        self.ui.deleteUserBtn.setEnabled(False)

    def start_edit_mode(self):
        self.is_new_user_mode = False
        self.ui.deleteUserBtn.setEnabled(True)

    def bind_methods(self):
        self.ui.clearUserSearchFieldBtn.clicked.connect(self.clear_search_user_fields)
        self.ui.searchUserBtn.clicked.connect(self.search_user)
        self.ui.editSelectedUserBtn.clicked.connect(self.edit_user)
        self.ui.deleteUserBtn.clicked.connect(self.delete_user)
        self.ui.createNewUserBtn.clicked.connect(self.create_new_user)
        self.ui.saveUserBtn.clicked.connect(self.save_user)

    def clear_search_user_fields(self):
        self.ui.searchFirstnameLineEdit.setText("")
        self.ui.searchLastnameLineEdit.setText("")
        self.ui.searchMiddlenameLineEdit.setText("")

    def search_user(self):
        try:
            user_service = UserService(self.application.conn)
            self.users = user_service.get_list_by_search_conditions(
                firstname=self.ui.searchFirstnameLineEdit.text(),
                lastname=self.ui.searchLastnameLineEdit.text(),
                middlename=self.ui.searchMiddlenameLineEdit.text(),
            )
            self.update_user_list()
        except ConnectionError:
            return

    def update_user_list(self):
        self.ui.userList.clear()
        self.ui.userList.addItems(
            [f"{user.lastname} {user.firstname} {user.middlename} ({user.id})" for user in self.users]
        )

    def clear_user_form(self):
        self.ui.bookHistoryList.clear()
        self.ui.firstnameLineEdit.setText("")
        self.ui.lastnameLineEdit.setText("")
        self.ui.middlenameLineEdit.setText("")
        self.ui.phoneLineEdit.setText("")
        self.ui.registerDateLabel.setText("")
        self.current_user = None

    def create_new_user(self):
        self.start_new_mode()
        self.clear_user_form()

    def edit_user(self):
        if not self.ui.userList.selectedItems():
            QMessageBox.critical(
                self.application, "Ошибка", "Пользователь не выбран", QMessageBox.Ok
            )
            return
        self.start_edit_mode()
        index = self.ui.userList.currentRow()
        self.current_user = self.users[index]
        try:
            user_service = UserService(self.application.conn)
            book_history_list = user_service.get_user_book_history(self.current_user.id)
            self.ui.bookHistoryList.clear()
            self.ui.bookHistoryList.addItems(
                [f"{str(book.take_date)} - {book.name} ({'возвращена' if book.is_returned else 'на руках'})"
                 for book in book_history_list]
            )
            self.ui.firstnameLineEdit.setText(self.current_user.firstname)
            self.ui.lastnameLineEdit.setText(self.current_user.lastname)
            self.ui.middlenameLineEdit.setText(self.current_user.middlename)
            self.ui.phoneLineEdit.setText(self.current_user.phone)
            self.ui.registerDateLabel.setText(str(self.current_user.register_date))
        except ConnectionError:
            return

    def delete_user(self):
        try:
            user_service = UserService(self.application.conn)
            user_service.delete(self.current_user.id)
            self.users = list(filter(lambda user: user.id != self.current_user.id, self.users))
            self.update_user_list()
            self.current_user = None
            self.clear_user_form()
            QMessageBox.information(
                self.application, "Удаление завершено", "Пользователь успешно удален", QMessageBox.Ok
            )
        except ConnectionError:
            return

    def save_user(self):
        new_firstname = self.ui.firstnameLineEdit.text()
        new_lastname = self.ui.lastnameLineEdit.text()
        new_middlename = self.ui.middlenameLineEdit.text()
        new_phone = self.ui.phoneLineEdit.text()
        try:
            user_service = UserService(self.application.conn)
            if self.is_new_user_mode:
                self.save_new_user(user_service, new_firstname, new_lastname, new_middlename, new_phone)
            else:
                self.save_updated_user(user_service, new_firstname, new_lastname, new_middlename, new_phone)
        except ConnectionError:
            return

    def save_new_user(self, user_service, new_firstname, new_lastname, new_middlename, new_phone):
        user = InUser(
            firstname=new_firstname,
            lastname=new_lastname,
            middlename=new_middlename,
            phone=new_phone,
        )

        user_service.create(user)
        self.clear_user_form()
        QMessageBox.information(
            self.application, "Создание завершено", "Пользователь успешно создан", QMessageBox.Ok
        )

    def save_updated_user(self, user_service, new_firstname, new_lastname, new_middlename, new_phone):
        self.current_user.firstname = new_firstname
        self.current_user.lastname = new_lastname
        self.current_user.middlename = new_middlename
        self.current_user.phone = new_phone
        user_service.update(self.current_user)

        for (index, user) in enumerate(self.users):
            if user.id == self.current_user.id:
                self.users[index] = self.current_user
                break
        self.update_user_list()

        self.clear_user_form()
        self.current_user = None
        self.start_new_mode()
        QMessageBox.information(
            self.application, "Редактирование завершено",
            "Данные о пользователе успешно сохранены", QMessageBox.Ok
        )
