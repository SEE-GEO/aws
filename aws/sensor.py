import numpy as np
from parts.sensor import PassiveSensor, ActiveSensor

class AWS(PassiveSensor):
    def __init__(self,
                 f_grid):
        self.sensor_pos = np.array
        super().__init__("aws", f_grid, stokes_dimension=2)
        self.sensor_position = np.array([[600e3]])
        self.sensor_line_of_sight = np.arange(135, 181, 5).reshape(-1, 1)

class CloudSat(ActiveSensor):
    def __init__(self):
        range_bins = np.arange(500.0, 18e3 + 1.0, 500.0)
        super().__init__("cloudsat",
                         f_grid = np.array([94.1e9]),
                         stokes_dimension = 1)
        self.instrument_pol       = [1]
        self.instrument_pol_array = [[1]]
        self.extinction_scaling   = 1.0
        self.y_min = -30.0
        self.sensor_position = np.array([[600e3]])
        self.sensor_line_of_sight = np.array([[180.0]])
        self.nedt = 1.0


