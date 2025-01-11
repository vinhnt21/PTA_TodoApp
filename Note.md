# Cấu trúc dự án

```plaintext
│
├── models/
│   ├── user_manager.py # Class UserManager
│   ├── user.py         # Class User
│   └── todo.py         # Class Todo
│
├── ui/
│   ├── login.ui        # Giao diện đăng nhập
│   ├── register.ui     # Giao diện đăng ký
│   ├── todo.ui         # Giao diện todo list
│   ├── login_window.py # Logic cho màn login
│   ├── register_window.py  # Logic cho màn register
│   └── todo_window.py  # Logic cho màn todo
│
├── main.py             # File chạy chính
```

# Prompt Mẫu

```plaintext
Tôi đang làm 1 app với PyQT6 và QT Designer
Tôi sẽ dùng python load các file .ui và thêm logic vào đó

File ui của
 tôi có:
{Liệt kê các thành phần trong file .ui}

Nhiệm vụ: Cung cấp code style sheet theo yêu cầu để tôi thêm vào file ui, chỉ trả về style sheet

Yêu cầu:
{Yêu cầu cụ thể}

```
