from pathlib import Path

from rocketpy import SolidMotor


class SimulationMotor:
    motor = SolidMotor
    def getValue(self,actualFile):
        temps = []
        poussées = []

        with open(actualFile, 'r') as fichier:
            lignes = fichier.readlines()

            # Ignorer la première ligne qui contient des métadonnées
            for ligne in lignes[2:]:  # Commence à la deuxième ligne
                parties = ligne.split()
                if len(parties) >= 2:
                    temps.append(float(parties[0]))
                    poussées.append(float(parties[1]))

        # Retourner une liste de listes [temps, poussée]
        return [[t, p] for t, p in zip(temps, poussées)]
        # Alternative avec NumPy : return np.array(list(zip(temps, poussées)))

    def __init__(self):
        thrust_source_path = Path(__file__).parents[2] / "Data/Motors/Cesaroni/SIRIUS11.eng"

        self.set_motor(SolidMotor(
            thrust_source=self.getValue(thrust_source_path),
            dry_mass=1.815,
            dry_inertia=(0.125, 0.125, 0.002),
            center_of_dry_mass_position=0.317,
            grains_center_of_mass_position=0.397,
            burn_time=3.9,
            grain_number=5,
            grain_separation=0.005,
            grain_density=1815,
            grain_outer_radius=0.033,
            grain_initial_inner_radius=0.015,
            grain_initial_height=0.12,
            nozzle_radius=0.033,
            throat_radius=0.011,
            interpolation_method="linear",
            nozzle_position=0,
            coordinate_system_orientation="nozzle_to_combustion_chamber"
        ))

    def set_motor(self, new_motor):
        self.motor = new_motor
