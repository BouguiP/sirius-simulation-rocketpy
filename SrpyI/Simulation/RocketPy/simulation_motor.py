from pathlib import Path
from rocketpy import LiquidMotor, Fluid, CylindricalTank, MassBasedTank, Function
import numpy as np

class SimulationMotor:
    motor = LiquidMotor

    def getValue(self, actualFile):
        temps = []
        poussées = []

        with open(actualFile, 'r') as fichier:
            lignes = fichier.readlines()

            for ligne in lignes[2:]:
                parties = ligne.split()
                if len(parties) >= 2:
                    temps.append(float(parties[0]))
                    poussées.append(float(parties[1]))

        thrust_data = [[t, p] for t, p in zip(temps, poussées)]
        print(f"Thrust data read from file: {thrust_data[:5]}... (first 5 entries)")
        return thrust_data

    def __init__(self, thrust_file="SIRIUS11.eng"):
        thrust_source_path = Path(__file__).parents[2] / "Data/Motors/Cesaroni" / thrust_file
        print(f"Attempting to read thrust file: {thrust_source_path}")
        thrust_data = self.getValue(thrust_source_path)

        if not thrust_data or len(thrust_data) < 2:
            raise ValueError("Thrust data is empty or invalid. Please check the thrust file SIRIUS11.eng.")

        t_burn = 7.205

        propellant_liquid = Fluid(name="propellant_liquid", density=1000)
        propellant_gas = Fluid(name="propellant_gas", density=1.2)

        tank_shape = CylindricalTank(radius=0.1524, height=1.621, spherical_caps=False)

        m_prop = 17.059
        liquid_mass = Function([(0, m_prop), (t_burn, 0)], 'time (s)', 'liquid mass (kg)', 'linear')
        gas_mass = Function(lambda t: 0, 'time (s)', 'gas mass (kg)', 'constant')

        tank = MassBasedTank(
            name="propellant tank",
            geometry=tank_shape,
            flux_time=t_burn,
            gas=propellant_gas,
            liquid=propellant_liquid,
            gas_mass=gas_mass,
            liquid_mass=liquid_mass,
            discretize=100
        )

        motor = LiquidMotor(
            thrust_source=thrust_data,
            dry_mass=19.791,
            dry_inertia=(9.738, 9.735, 0.076),
            center_of_dry_mass_position=2.49012763,
            burn_time=t_burn,
            nozzle_radius=0.047588,
            nozzle_position=3.52946029,
            coordinate_system_orientation="nozzle_to_combustion_chamber"
        )

        motor.add_tank(tank, position=1.295)

        self.motor = motor
        print(f"Motor initialized: {type(self.motor)}")