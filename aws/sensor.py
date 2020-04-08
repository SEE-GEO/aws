import numpy as np
from artssat.sensor import PassiveSensor, ActiveSensor

class AWS(PassiveSensor):
    def __init__(self,
                 f_grid):
        self.sensor_pos = np.array
        super().__init__("aws", f_grid, stokes_dimension=2)
        self.sensor_line_of_sight = np.arange(135, 181, 5).reshape(-1, 1)
        self.sensor_position = np.broadcast_to(np.array([[600e3]]),
                                               self.sensor_line_of_sight.shape)

class ATMS(PassiveSensor):

    def __init__(self):
        f_grid = np.array([166.5,])
        f_grid = np.concatenate(f_grid, 183.31 + np.array([-7,-4.5,-3.0,-1.8,-1.0]))
        f_grid *= 1e9
        super().__init__("atms", f_grid, stokes_dimension=2)
        self.sensor_line_of_sight = np.arange(135, 181, 5).reshape(-1, 1)
        self.sensor_position = np.broadcast_to(np.array([[830e3]]),
                                               self.sensor_line_of_sight.shape)


class CloudSat(ActiveSensor):
    def __init__(self):
        range_bins = np.arange(500.0, 18e3 + 1.0, 500.0)
        super().__init__("cloudsat",
                         f_grid = np.array([94.1e9]),
                         stokes_dimension = 1)
        self.instrument_pol       = [1]
        self.instrument_pol_array = [[1]]
        self.extinction_scaling   = 0.0
        self.y_min = -30.0
        self.sensor_position = np.array([[600e3]])
        self.sensor_line_of_sight = np.array([[180.0]])
        self.nedt = 1.0

band_166  = 166.50e9 + np.array([-0.8, 0.8]) * 1e9
band_183l = 183.31e9 + np.arange(-8.0, -0.8, 8.0) * 1e9;
band_229  = 229.00e9 + np.array([-1.0, 1.0]) * 1e9;
band_325l = 325.15e9 + np.arange(-9.0, -0.75, 8.0) * 1e9;
band_325u = 325.15e9 + np.arange(0.75, 9.0, 8.0) * 1e9;
