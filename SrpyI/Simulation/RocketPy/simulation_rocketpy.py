from rocketpy import Environment
import datetime


class SimulationRocketPy:
    launch_environment = Environment()

    def __init__(self):
        launch_date = datetime.date.today()
        launch_hour = 12
        launch_timezone = "EST"

        self.set_launch_date(launch_date, launch_hour, launch_timezone)

    def set_launch_date(self, date, hour, timezone):
        if not isinstance(date, date):
            print("Expected type is date; received type is " + str(type(date)))

        self.launch_environment.set_date(
            (date.year, date.month, date.day, hour),
            timezone=timezone
        )
