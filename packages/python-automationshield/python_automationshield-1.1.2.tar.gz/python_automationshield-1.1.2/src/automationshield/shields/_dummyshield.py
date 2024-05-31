import numpy as np
import time

from .baseshield import BaseShield


class DummyShield(BaseShield):
    """Dummy class that mimicks Shield interface. Used for testing when no hardware is available."""
    class PlotInfo:
        sensor_unit = r"$\degree$"
        sensor_type = "Angle"
        sensor_min = 0
        sensor_max = 180

    def __init__(self) -> None:
        pass

    def read(self) -> tuple[float]:
        ti = time.perf_counter()

        pot = 100 + 50*np.sin(ti)
        sensor = 100 + 125*np.cos(ti)

        return pot, sensor

    def write(self, flag: int, actuator: float):
        return self.saturate_bits(actuator, self.actuator_bits)

    def open(self):
        return self

    def close(self, *args):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

