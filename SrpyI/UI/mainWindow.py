from PyQt5.QtWidgets import QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sirius Rpy Interface")
        button = QPushButton("Test")

        self.setCentralWidget(button)