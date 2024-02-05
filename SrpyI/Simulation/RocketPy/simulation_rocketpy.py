from rocketpy import Environment
from SrpyI.Simulation.RocketPy.simulation_motor import SimulationMotor
import datetime


class SimulationRocketPy:
    launch_environment = Environment()
    # rocket_motor = SimulationMotor()

    def __init__(self):
        launch_date = datetime.date.today() + datetime.timedelta(days=1)
        launch_hour = 12
        launch_timezone = "EST"

        self.set_launch_date(launch_date, launch_hour, launch_timezone)
        self.set_atmospheric_model("Forecast", "GFS")

    def set_launch_date(self, date, hour, timezone):
        if not isinstance(date, type(datetime.date)):
            print("Expected type is date; received type is " + str(type(date)))

        self.launch_environment.set_date(
            (date.year, date.month, date.day, hour),
            timezone=timezone
        )

    def set_atmospheric_model(self, model_type, file):
        self.launch_environment.set_atmospheric_model(type=model_type, file=file)
