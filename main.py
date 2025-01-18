from PyQt6.QtWidgets import *
import sys
from ui.login_window import LoginWindow
from ui.register_window import RegisterWindow
from ui.main_window import MainWindow
from models.user_manager import UserManager


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow()
        self.register_window = RegisterWindow()
        self.todo_window = None  # Sẽ được tạo sau khi login

        # Data
        self.user_manager = UserManager()
        self.user = None

        # Kết nối các sự kiện với các hàm xử lý
        # login
        self.login_window.btn_open_register_window.clicked.connect(self.open_register)
        self.login_window.btn_login.clicked.connect(self.login)
        # register
        self.register_window.btn_open_login_window.clicked.connect(self.open_login)
        self.register_window.btn_register.clicked.connect(self.register)

    def init_todo(self):
        self.todo_window.btn_add_todo.clicked.connect(self.add_todo)
        self.todo_window.btn_set_done.clicked.connect(self.set_done)
        self.todo_window.btn_set_not_done.clicked.connect(self.set_not_done)

    def run(self):
        self.login_window.show()
        return self.app.exec()

    # login
    def open_register(self):
        self.register_window.show()

    def login(self):
        username = self.login_window.input_username.text()
        password = self.login_window.input_password.text()

        result = self.user_manager.check_user(username, password)
        if result["status"]:
            QMessageBox.information(self.login_window, "Success", result["message"])
            # Xử lý tiếp
            self.todo_window = MainWindow()
            self.todo_window.show()
            self.login_window.hide()
            self.user = result["user"]
            self.init_todo()
        else:
            QMessageBox.critical(self.login_window, "Error", result["message"])

    # register
    def open_login(self):
        self.login_window.show()
        self.register_window.hide()

    def register(self):
        username = self.register_window.input_username.text()
        password = self.register_window.input_password.text()
        confirm_password = self.register_window.input_confirm_password.text()
        if password != confirm_password:
            QMessageBox.critical(self.register_window, "Error", "Mật khẩu không khớp")
        result = self.user_manager.add_user(username, password)
        if result["status"]:
            QMessageBox.information(self.register_window, "Success", result["message"])
        else:
            QMessageBox.critical(self.register_window, "Error", result["message"])

    # todo
    def add_todo(self):
        title_todo = self.todo_window.lineEdit.text()
        description_todo = self.todo_window.textEdit.toPlainText()
        if not title_todo:
            QMessageBox.critical(
                self.todo_window, "Error", "Tiêu đề không được để trống"
            )
            return

        for todo in self.user.todo_manager:
            if todo.title == title_todo:
                QMessageBox.critical(
                    self.todo_window, "Error", "Tiêu đề công việc đã tồn tại"
                )
                return

        self.user.add_todo(title_todo, description_todo)
        QMessageBox.information(
            self.todo_window, "Success", "Thêm công việc thành công"
        )

        self.todo_window.todo_list_widget.addItem(title_todo)

    def set_done(self):
        # get item selected from todo_list_widget
        todo_title = self.todo_window.todo_list_widget.currentItem().text()
        for todo in self.user.todo_manager:
            if todo.title == todo_title:
                todo.is_done = True
                break

        QMessageBox.information(self.todo_window, "Success", "Đã hoàn thành công việc")
        # remove item from todo_list_widget
        self.todo_window.todo_list_widget.takeItem(
            self.todo_window.todo_list_widget.currentRow()
        )

        # add item to done_list_widget
        self.todo_window.done_list_widget.addItem(todo_title)

    def set_not_done(self):
        # get item selected from done_list_widget
        todo_title = self.todo_window.done_list_widget.currentItem().text()
        for todo in self.user.todo_manager:
            if todo.title == todo_title:
                todo.is_done = False
                break

        QMessageBox.information(self.todo_window, "Success", "Đã hoàn thành công việc")
        # remove item from done_list_widget
        self.todo_window.done_list_widget.takeItem(
            self.todo_window.done_list_widget.currentRow()
        )

        # add item to todo_list_widget
        self.todo_window.todo_list_widget.addItem(todo_title)


if __name__ == "__main__":
    app = App()
    sys.exit(app.run())
