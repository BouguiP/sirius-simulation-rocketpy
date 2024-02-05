from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from SrpyI.UI.PyQt.mainWindow import MainWindow
from SrpyI.Simulation.RocketPy.simulation_rocketpy import SimulationRocketPy

from rocketpy import Environment, Rocket, SolidMotor, Flight

import sys

app = QApplication(sys.argv)
window = MainWindow()
window.set_active_window("")
window.show()

app.exec()

simulation = SimulationRocketPy()


