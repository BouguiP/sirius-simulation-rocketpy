from pathlib import Path

from rocketpy import SolidMotor


class SimulationMotor:
    motor = SolidMotor

    def __init__(self):
        thrust_source_path = Path(__file__).parents[2] / "Data/Motors/Cesaroni/M1670-BS.eng"

        self.set_motor(SolidMotor(
            thrust_source=thrust_source_path,
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
