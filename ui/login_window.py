from PyQt6 import uic
from PyQt6.QtWidgets import *


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)
