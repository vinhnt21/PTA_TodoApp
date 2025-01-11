from PyQt6.QtWidgets import *
import sys
from ui.login_window import LoginWindow
from ui.register_window import RegisterWindow
from models.user_manager import UserManager


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow()
        self.register_window = RegisterWindow()
        self.todo_window = None  # Sẽ được tạo sau khi login

        # Data
        self.user_manager = UserManager()
        self.todo_manager = None  # Sẽ được tạo sau khi login

        # Kết nối các sự kiện với các hàm xử lý
        # login
        self.login_window.btn_open_register_window.clicked.connect(self.open_register)
        self.login_window.btn_login.clicked.connect(self.login)
        # register
        self.register_window.btn_open_login_window.clicked.connect(self.open_login)
        self.register_window.btn_register.clicked.connect(self.register)

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


if __name__ == "__main__":
    app = App()
    sys.exit(app.run())
