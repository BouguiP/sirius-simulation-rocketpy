from rocketpy import Environment, Rocket, Flight
from Simulation.RocketPy.simulation_motor import SimulationMotor
import datetime
import numpy as np
import matplotlib.pyplot as plt

class SimulationRocketPy:
    def __init__(self):
        # Définir les coordonnées de lancement
        self.launch_environment = Environment(
            latitude=47.96577546457938,
            longitude=-81.87433964833036,
            elevation=1400  # Garder l'élévation par défaut ou ajuster si nécessaire
        )
        self.rocket_motor = SimulationMotor()
        launch_date = datetime.date.today() + datetime.timedelta(days=1)
        launch_hour = 12
        launch_timezone = "EST"
        self.set_launch_date(launch_date, launch_hour, launch_timezone)
        # Commenter le modèle GFS pour tester avec le vent personnalisé
        # self.set_atmospheric_model("Forecast", "GFS")

    def set_launch_date(self, date, hour, timezone):
        if not isinstance(date, type(datetime.date)):
            print("Expected type is date; received type is " + str(type(date)))
        self.launch_environment.set_date(
            (date.year, date.month, date.day, hour),
            timezone=timezone
        )

    def set_atmospheric_model(self, model_type, file):
        self.launch_environment.set_atmospheric_model(type=model_type, file=file)

