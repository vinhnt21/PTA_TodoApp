class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.todos = []  # List các todo của user
