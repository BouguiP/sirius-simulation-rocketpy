import numpy as np
from rocketpy import Environment, Rocket, SolidMotor, Flight, Function
import matplotlib.pyplot as plt
from Simulation.RocketPy.simulation_rocketpy import SimulationRocketPy
from Simulation.RocketPy.simulation_motor import SimulationMotor

class MonteCarloDispersion:
    def __init__(self, num_simulations=1000):
        self.num_simulations = num_simulations
        self.sim_rocketpy = SimulationRocketPy()
        self.sim_motor = SimulationMotor()
        self.landings = []

    def run_monte_carlo(self):
        # Définir la fusée
        rocket = Rocket(
            radius=0.05124,
            mass=55,
            inertia=(36.904, 36.904, 0.221),
            power_off_drag=0.4,
            power_on_drag=0.4,
            center_of_mass_without_motor=2.152,
            coordinate_system_orientation="nose_to_tail"
        )

        # Ajouter le nez conique (von Karman)
        rocket.add_nose(
            length=0.55829,
            kind="von karman",
            position=0
        )

        # Ajouter les ailerons trapézoïdaux
        rocket.add_trapezoidal_fins(
            n=4,
            root_chord=0.120,
            tip_chord=0.060,
            span=0.110,
            position=2.5,
            cant_angle=0.5
        )

        # Ajouter la queue conique
        rocket.add_tail(
            top_radius=0.0635,
            bottom_radius=0.0435,
            length=0.060,
            position=1.305344
        )

        # Ajouter le moteur
        rocket.add_motor(self.sim_motor.motor, position=2.5)

        # Vérifier la stabilité de la fusée
        print("Vérification de la stabilité de la fusée...")
        rocket.all_info()  # Affiche les informations sur la fusée, y compris la stabilité

        # Désactiver temporairement le parachute pour tester
        # rocket.add_parachute(
        #     name="main",
        #     cd_s=1.0,
        #     trigger="apogee"
        # )

        # Récupérer l'environnement
        env = self.sim_rocketpy.launch_environment

        # Tester une seule simulation avec des paramètres fixes
        print("Lancement d'une simulation test unique...")
        thrust_factor = 1.0  # Poussée nominale
        self.sim_motor.motor.thrust_source = [
            [t, p * thrust_factor] for t, p in self.sim_motor.motor.thrust_source
        ]
        inclination = 85  # Angle fixe
        azimuth = 0  # Direction fixe
        wind_speed = 0  # Vent nul pour simplifier
        wind_direction = 0
        wind_u = wind_speed * np.cos(np.radians(wind_direction))
        wind_v = wind_speed * np.sin(np.radians(wind_direction))

        env.wind_velocity_x = Function(lambda alt: wind_u, interpolation="linear")
        env.wind_velocity_y = Function(lambda alt: wind_v, interpolation="linear")

        # Simuler le vol
        flight = Flight(
            rocket=rocket,
            environment=env,
            inclination=inclination,
            heading=azimuth,
            rail_length=5.6388,
            max_time=100
        )

        # Si la simulation unique fonctionne, on peut réactiver Monte Carlo
        print("Simulation unique terminée avec succès. Lancement des simulations Monte Carlo...")
        for i in range(self.num_simulations):
            print(f"Simulation {i+1}/{self.num_simulations}")

            thrust_factor = np.random.normal(1.0, 0.05)
            self.sim_motor.motor.thrust_source = [
                [t, p * thrust_factor] for t, p in self.sim_motor.motor.thrust_source
            ]
            inclination = np.random.normal(85, 1)
            azimuth = np.random.uniform(0, 360)
            wind_speed = np.random.normal(2, 0.5)
            wind_direction = np.random.uniform(0, 360)
            wind_u = wind_speed * np.cos(np.radians(wind_direction))
            wind_v = wind_speed * np.sin(np.radians(wind_direction))

            env.wind_velocity_x = Function(lambda alt: wind_u, interpolation="linear")
            env.wind_velocity_y = Function(lambda alt: wind_v, interpolation="linear")

            flight = Flight(
                rocket=rocket,
                environment=env,
                inclination=inclination,
                heading=azimuth,
                rail_length=5.6388,
                max_time=100
            )

            landing_lat = flight.latitude[-1]
            landing_lon = flight.longitude[-1]
            self.landings.append((landing_lat, landing_lon))

    def plot_dispersion(self):
        landings_array = np.array(self.landings)
        plt.figure(figsize=(10, 10))
        plt.scatter(landings_array[:, 1], landings_array[:, 0], s=10, alpha=0.5, label="Points de chute")
        launch_lat = self.sim_rocketpy.launch_environment.latitude
        launch_lon = self.sim_rocketpy.launch_environment.longitude
        plt.scatter(launch_lon, launch_lat, color="red", s=100, marker="x", label="Point de lancement")
        plt.xlabel("Longitude (degrés)")
        plt.ylabel("Latitude (degrés)")
        plt.title(f"Dispersion des points de chute ({self.num_simulations} simulations)")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    mc_analysis = MonteCarloDispersion(num_simulations=500)
    mc_analysis.run_monte_carlo()
    mc_analysis.plot_dispersion()