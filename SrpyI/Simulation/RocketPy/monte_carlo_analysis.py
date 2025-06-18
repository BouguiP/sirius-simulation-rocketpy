import numpy as np
from rocketpy import Environment, Rocket, LiquidMotor, Flight, Function
import matplotlib.pyplot as plt
from .simulation_rocketpy import SimulationRocketPy
from .simulation_motor import SimulationMotor

class MonteCarloDispersion:
    def __init__(self, num_simulations=1000, thrust_file="SIRIUS11.eng"):
        self.num_simulations = num_simulations
        self.sim_rocketpy = SimulationRocketPy()
        self.sim_motor = SimulationMotor(thrust_file=thrust_file)
        self.landings = []

    def run_monte_carlo(self):
        rocket = Rocket(
            radius=0.1524,
            mass=11.608,
            inertia=(19.87229886, 19.87217723, 0.07508979),
            power_off_drag=0.6,
            power_on_drag=0.54,
            center_of_mass_without_motor=1.83912056,
            coordinate_system_orientation="nose_to_tail"
        )

        rocket.add_nose(length=0.4572, kind="von karman", position=0)
        rocket.add_trapezoidal_fins(
            n=4,
            root_chord=0.4064,
            tip_chord=0.1524,
            span=0.1524,
            position=2.5,
            cant_angle=2
        )
        # Pas de queue

        rocket.add_parachute(name="main", cd_s=2.0, trigger="apogee")

        print("Vérification du moteur...")
        print(f"Motor type before attachment: {type(self.sim_motor.motor)}")
        if not isinstance(self.sim_motor.motor, LiquidMotor):
            raise ValueError("Erreur : self.sim_motor.motor n'est pas un LiquidMotor valide.")
        rocket.add_motor(self.sim_motor.motor, position=2.5)

        print("Vérification de la stabilité de la fusée...")
        rocket.all_info()

        env = self.sim_rocketpy.launch_environment

        print("Lancement d'une simulation test unique...")
        thrust_factor = 1.0
        self.sim_motor.motor.thrust_source = [[t, p * thrust_factor] for t, p in self.sim_motor.motor.thrust_source]
        inclination = 85
        azimuth = 0
        wind_speed = 0
        wind_direction = 0
        wind_u = wind_speed * np.cos(np.radians(wind_direction))
        wind_v = wind_speed * np.sin(np.radians(wind_direction))

        env.wind_velocity_x = Function(lambda alt: wind_u, interpolation="linear")
        env.wind_velocity_y = Function(lambda alt: wind_v, interpolation="linear")

        flight = Flight(
            rocket=rocket, environment=env, inclination=inclination, heading=azimuth,
            rail_length=5.6388, max_time=50, rtol=1e-3, atol=1e-3
        )

        print("Simulation unique terminée avec succès. Lancement des simulations Monte Carlo...")
        for i in range(self.num_simulations):
            print(f"Simulation {i+1}/{self.num_simulations}")

            thrust_factor = np.random.normal(1.0, 0.1)
            self.sim_motor.motor.thrust_source = [[t, p * thrust_factor] for t, p in self.sim_motor.motor.thrust_source]
            inclination = np.random.normal(85, 2)
            azimuth = np.random.uniform(0, 360)
            wind_speed = np.random.normal(5, 1)
            wind_direction = np.random.uniform(0, 360)
            wind_u = wind_speed * np.cos(np.radians(wind_direction))
            wind_v = wind_speed * np.sin(np.radians(wind_direction))

            env.wind_velocity_x = Function(lambda alt: wind_u, interpolation="linear")
            env.wind_velocity_y = Function(lambda alt: wind_v, interpolation="linear")

            flight = Flight(
                rocket=rocket, environment=env, inclination=inclination, heading=azimuth,
                rail_length=5.6388, max_time=50, rtol=1e-3, atol=1e-3
            )

            # Correction de l'extraction des coordonnées
            landing_lat = flight.latitude[-1][1]  # Deuxième élément pour la latitude
            landing_lon = flight.longitude[-1][1]  # Deuxième élément pour la longitude
            self.landings.append((landing_lat, landing_lon))
            print(f"Simulation {i+1}: Landing point (lat, lon) = ({landing_lat}, {landing_lon})")

    def plot_dispersion(self):
        print(f"Nombre de points de chute : {len(self.landings)}")
        if len(self.landings) == 0:
            print("Erreur : Aucun point de chute n'a été généré. Vérifiez si les simulations Monte Carlo se terminent correctement.")
            return

        landings_array = np.array(self.landings)
        print(f"Points de chute (lat, lon) : {landings_array}")
        launch_lat = self.sim_rocketpy.launch_environment.latitude
        launch_lon = self.sim_rocketpy.launch_environment.longitude
        print(f"Point de lancement (lat, lon) : ({launch_lat}, {launch_lon})")

        if np.any(np.isnan(landings_array)):
            print("Attention : Les données contiennent des valeurs NaN, ce qui peut causer un graphique blanc.")
            return

        plt.figure(figsize=(10, 10))
        plt.scatter(landings_array[:, 1], landings_array[:, 0], s=50, alpha=0.7, label="Points de chute")
        plt.scatter(launch_lon, launch_lat, color="red", s=200, marker="x", label="Point de lancement")
        plt.xlabel("Longitude (degrés)")
        plt.ylabel("Latitude (degrés)")
        plt.title(f"Dispersion des points de chute ({self.num_simulations} simulations)")

        # Zoom avec une marge encore plus petite
        if len(landings_array) > 0:
            lon_min = min(launch_lon, np.min(landings_array[:, 1])) - 0.0005  # Marge réduite à 0.0005 degré
            lon_max = max(launch_lon, np.max(landings_array[:, 1])) + 0.0005
            lat_min = min(launch_lat, np.min(landings_array[:, 0])) - 0.0005
            lat_max = max(launch_lat, np.max(landings_array[:, 0])) + 0.0005
            plt.xlim(lon_min, lon_max)
            plt.ylim(lat_min, lat_max)

        plt.legend()
        plt.grid(True)
        plt.savefig("dispersion_plot.png")
        print("Graphique sauvegardé sous 'dispersion_plot.png'")
        plt.show()