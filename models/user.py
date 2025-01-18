from models.todo import Todo


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.todo_manager = []

    def add_todo(self, title, description):
        self.todo_manager.append(Todo(title, description))
