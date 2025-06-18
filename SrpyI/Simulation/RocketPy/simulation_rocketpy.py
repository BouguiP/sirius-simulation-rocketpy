from rocketpy import Environment
import datetime
import numpy as np
import matplotlib.pyplot as plt

class SimulationRocketPy:
    def __init__(self):
        self.launch_environment = Environment(
            latitude=47.96577546457938,
            longitude=-81.87433964833036,
            elevation=1400
        )
        launch_date = datetime.date.today() + datetime.timedelta(days=1)
        launch_hour = 12
        launch_timezone = "EST"
        self.set_launch_date(launch_date, launch_hour, launch_timezone)

    def set_launch_date(self, date, hour, timezone):
        if not isinstance(date, datetime.date):  # Correction de la vérification
            print("Expected type is datetime.date; received type is " + str(type(date)))
        self.launch_environment.set_date(
            (date.year, date.month, date.day, hour),
            timezone=timezone
        )

    def set_atmospheric_model(self, model_type, file):
        self.launch_environment.set_atmospheric_model(type=model_type, file=file)