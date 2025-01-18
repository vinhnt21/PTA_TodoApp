from models.user import User


class UserManager:
    def __init__(self):
        self.users = [User("admin", "admin")]

    def add_user(self, username, password):
        if not username or not password:
            return {
                "status": False,
                "message": "Tên đăng nhập hoặc mật khẩu không được để trống",
            }
        for user in self.users:
            if user.username == username:
                return {"status": False, "message": "Tên đăng nhập đã tồn tại"}
        user = User(username, password)
        self.users.append(user)

        return {"status": True, "message": "Đăng ký thành công"}

    def check_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return {"status": True, "message": "Đăng nhập thành công", "user": user}
        return {"status": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng"}
