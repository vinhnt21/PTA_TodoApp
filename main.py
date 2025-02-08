from PyQt6.QtWidgets import *
import sys
from ui.login_window import LoginWindow
from ui.register_window import RegisterWindow
from ui.main_window import MainWindow
from models.user_manager import UserManager


class App:
    """
    Lớp chính của ứng dụng, quản lý tất cả các cửa sổ và logic nghiệp vụ
    """

    def __init__(self):
        """
        Khởi tạo ứng dụng với các cửa sổ và dữ liệu cần thiết
        """
        # Khởi tạo ứng dụng Qt
        self.app = QApplication(sys.argv)

        # Khởi tạo các cửa sổ
        self.login_window = LoginWindow()
        self.register_window = RegisterWindow()
        self.todo_window = None  # Sẽ được tạo sau khi đăng nhập thành công

        # Khởi tạo dữ liệu
        self.user_manager = UserManager()  # Quản lý người dùng
        self.user = None  # Người dùng hiện tại

        # Thiết lập các kết nối sự kiện
        self.setup_login_connections()
        self.setup_register_connections()

    def setup_login_connections(self):
        """
        Thiết lập các kết nối sự kiện cho cửa sổ đăng nhập
        """
        # Kết nối nút mở form đăng ký
        self.login_window.btn_open_register_window.clicked.connect(self.open_register)
        # Kết nối nút đăng nhập
        self.login_window.btn_login.clicked.connect(self.login)
        # Kết nối phím Enter ở ô password để đăng nhập
        self.login_window.input_password.returnPressed.connect(self.login)

    def setup_register_connections(self):
        """
        Thiết lập các kết nối sự kiện cho cửa sổ đăng ký
        """
        # Kết nối nút mở form đăng nhập
        self.register_window.btn_open_login_window.clicked.connect(self.open_login)
        # Kết nối nút đăng ký
        self.register_window.btn_register.clicked.connect(self.register)
        # Kết nối phím Enter ở ô xác nhận mật khẩu để đăng ký
        self.register_window.input_confirm_password.returnPressed.connect(self.register)

    def init_todo(self):
        """
        Khởi tạo các kết nối sự kiện cho cửa sổ todo sau khi đăng nhập
        """
        # Kết nối các nút chức năng
        self.todo_window.btn_add_todo.clicked.connect(self.add_todo)
        self.todo_window.btn_set_done.clicked.connect(self.set_done)
        self.todo_window.btn_set_not_done.clicked.connect(self.set_not_done)
        self.todo_window.lineEdit.returnPressed.connect(self.add_todo)

        # Kết nối sự kiện chọn item trong danh sách
        self.todo_window.todo_list_widget.itemSelectionChanged.connect(
            self.handle_todo_selection
        )
        self.todo_window.done_list_widget.itemSelectionChanged.connect(
            self.handle_done_selection
        )

        # Vô hiệu hóa các nút khi chưa chọn item
        self.todo_window.btn_set_done.setEnabled(False)
        self.todo_window.btn_set_not_done.setEnabled(False)

    def run(self):
        """
        Khởi chạy ứng dụng, hiển thị cửa sổ đăng nhập
        """
        self.login_window.show()
        return self.app.exec()

    def open_register(self):
        """
        Mở cửa sổ đăng ký và ẩn cửa sổ đăng nhập
        """
        self.register_window.show()
        self.login_window.hide()
        self.clear_login_inputs()

    def open_login(self):
        """
        Mở cửa sổ đăng nhập và ẩn cửa sổ đăng ký
        """
        self.login_window.show()
        self.register_window.hide()
        self.clear_register_inputs()

    def clear_login_inputs(self):
        """
        Xóa nội dung các ô input trong form đăng nhập
        """
        self.login_window.input_username.clear()
        self.login_window.input_password.clear()

    def clear_register_inputs(self):
        """
        Xóa nội dung các ô input trong form đăng ký
        """
        self.register_window.input_username.clear()
        self.register_window.input_password.clear()
        self.register_window.input_confirm_password.clear()

    def login(self):
        """
        Xử lý đăng nhập: kiểm tra thông tin và chuyển đến màn hình todo nếu thành công
        """
        # Lấy thông tin đăng nhập và loại bỏ khoảng trắng
        username = self.login_window.input_username.text().strip()
        password = self.login_window.input_password.text().strip()

        # Kiểm tra dữ liệu đầu vào
        if not username or not password:
            QMessageBox.warning(
                self.login_window, "Warning", "Vui lòng điền đầy đủ thông tin"
            )
            return

        # Kiểm tra thông tin đăng nhập
        result = self.user_manager.check_user(username, password)
        if result["status"]:
            QMessageBox.information(self.login_window, "Success", result["message"])
            self.user = result["user"]
            self.show_todo_window()
        else:
            QMessageBox.critical(self.login_window, "Error", result["message"])

    def show_todo_window(self):
        """
        Hiển thị cửa sổ todo sau khi đăng nhập thành công
        """
        self.todo_window = MainWindow()
        self.init_todo()
        self.load_todos()
        self.todo_window.show()
        self.login_window.hide()
        self.clear_login_inputs()

    def load_todos(self):
        """
        Tải danh sách công việc của người dùng hiện tại vào giao diện
        """
        for todo in self.user.todo_manager:
            if todo.completed:
                self.todo_window.done_list_widget.addItem(todo.title)
            else:
                self.todo_window.todo_list_widget.addItem(todo.title)

    def register(self):
        """
        Xử lý đăng ký tài khoản mới
        """
        # Lấy thông tin đăng ký và loại bỏ khoảng trắng
        username = self.register_window.input_username.text().strip()
        password = self.register_window.input_password.text().strip()
        confirm_password = self.register_window.input_confirm_password.text().strip()

        # Kiểm tra dữ liệu đầu vào
        if not username or not password or not confirm_password:
            QMessageBox.warning(
                self.register_window, "Warning", "Vui lòng điền đầy đủ thông tin"
            )
            return

        # Kiểm tra mật khẩu xác nhận
        if password != confirm_password:
            QMessageBox.critical(self.register_window, "Error", "Mật khẩu không khớp")
            return

        # Thực hiện đăng ký
        result = self.user_manager.add_user(username, password)
        if result["status"]:
            QMessageBox.information(self.register_window, "Success", result["message"])
            self.open_login()
        else:
            QMessageBox.critical(self.register_window, "Error", result["message"])

    def add_todo(self):
        """
        Thêm một công việc mới vào danh sách
        """
        # Lấy tiêu đề công việc và loại bỏ khoảng trắng
        title_todo = self.todo_window.lineEdit.text().strip()

        # Kiểm tra tiêu đề không được trống
        if not title_todo:
            QMessageBox.warning(
                self.todo_window, "Warning", "Tiêu đề không được để trống"
            )
            return

        # Kiểm tra tiêu đề không được trùng
        for todo in self.user.todo_manager:
            if todo.title.lower() == title_todo.lower():
                QMessageBox.critical(
                    self.todo_window, "Error", "Tiêu đề công việc đã tồn tại"
                )
                return

        # Thêm công việc mới
        self.user.add_todo(title_todo)
        self.todo_window.todo_list_widget.addItem(title_todo)
        self.todo_window.lineEdit.clear()

    def handle_todo_selection(self):
        """
        Xử lý khi chọn một công việc trong danh sách chưa hoàn thành
        """
        self.todo_window.btn_set_done.setEnabled(
            self.todo_window.todo_list_widget.currentItem() is not None
        )
        self.todo_window.btn_set_not_done.setEnabled(False)

    def handle_done_selection(self):
        """
        Xử lý khi chọn một công việc trong danh sách đã hoàn thành
        """
        self.todo_window.btn_set_not_done.setEnabled(
            self.todo_window.done_list_widget.currentItem() is not None
        )
        self.todo_window.btn_set_done.setEnabled(False)

    def set_done(self):
        """
        Đánh dấu một công việc là đã hoàn thành
        """
        current_item = self.todo_window.todo_list_widget.currentItem()
        if not current_item:
            return

        todo_title = current_item.text()
        # Cập nhật trạng thái công việc
        for todo in self.user.todo_manager:
            if todo.title == todo_title:
                todo.completed = True
                break

        # Cập nhật giao diện
        self.todo_window.todo_list_widget.takeItem(
            self.todo_window.todo_list_widget.currentRow()
        )
        self.todo_window.done_list_widget.addItem(todo_title)
        QMessageBox.information(self.todo_window, "Success", "Đã hoàn thành công việc")

    def set_not_done(self):
        """
        Đánh dấu một công việc là chưa hoàn thành
        """
        current_item = self.todo_window.done_list_widget.currentItem()
        if not current_item:
            return

        todo_title = current_item.text()
        # Cập nhật trạng thái công việc
        for todo in self.user.todo_manager:
            if todo.title == todo_title:
                todo.completed = False
                break

        # Cập nhật giao diện
        self.todo_window.done_list_widget.takeItem(
            self.todo_window.done_list_widget.currentRow()
        )
        self.todo_window.todo_list_widget.addItem(todo_title)
        QMessageBox.information(
            self.todo_window, "Success", "Đã đặt lại trạng thái chưa hoàn thành"
        )


if __name__ == "__main__":
    app = App()
    sys.exit(app.run())
