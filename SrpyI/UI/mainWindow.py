from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        # global parameters
        window_title = "Sirius RocketPy Interface"
        window_size = QSize(400, 300)

        button_size = QSize(120, 30)

        super().__init__()

        self.setWindowTitle(window_title)
        self.setFixedSize(window_size)

        button = QPushButton("Test")
        button.setFixedSize(button_size)

        self.setCentralWidget(button)
