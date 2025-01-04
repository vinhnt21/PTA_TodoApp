from PyQt6 import uic
from PyQt6.QtWidgets import *


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)
