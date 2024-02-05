# Lib dependencies
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout

# Custom dependencies
from SrpyI.UI.PyQt.motorContainer import MotorContainer


class MainWindow(QMainWindow):
    # window = QMainWindow()

    layout = QVBoxLayout()
    # motor_container = MotorContainer()

    def __init__(self):
        # global parameters
        window_title = "Sirius RocketPy Interface"
        window_size = QSize(400, 300)

        super().__init__()

        self.setWindowTitle(window_title)
        self.setFixedSize(window_size)

    def set_active_window(self, window_name):
        button_size = QSize(120, 30)

        button = QPushButton("Test")
        button.setFixedSize(button_size)

        self.setCentralWidget(button)

        # self.layout.addWidget(button)

        # self.setLayout(self.layout)
