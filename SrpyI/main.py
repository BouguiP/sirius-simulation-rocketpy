from PyQt5.QtWidgets import QApplication
from SrpyI.UI.PyQt.mainWindow import MainWindow

from rocketpy import Environment, Rocket, SolidMotor, Flight

import sys

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()


