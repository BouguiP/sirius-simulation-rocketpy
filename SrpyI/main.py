from PyQt5.QtWidgets import QApplication
from UI.PyQt.mainWindow import MainWindow
from Simulation.RocketPy.monte_carlo_analysis import MonteCarloDispersion
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.set_active_window("")
window.show()

app.exec()

# Lancer l'analyse Monte Carlo après la fermeture de la fenêtre (ou via un bouton dans l'UI)
mc_analysis = MonteCarloDispersion(num_simulations=100)
mc_analysis.run_monte_carlo()
mc_analysis.plot_dispersion()