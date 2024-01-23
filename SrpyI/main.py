from PyQt5.QtWidgets import QApplication
from UI.mainWindow import MainWindow

from rocketpy import Environment, Rocket, SolidMotor, Flight
import datetime

import sys

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
