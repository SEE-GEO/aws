import os
import numpy as np
from h5py import File
from artssat.data_provider import DataProviderBase

class Profiles(DataProviderBase):
    """
    Data provider class that provides the artssat interface for an
    input data file in HDF5 (matlab) format.

    Attributes:
        self.path: The filename of the input data
        self.data: HDF5 group object containing the data

    """
    def __init__(self, path):
        """
        Create data provider from given input file.

        Args:
            path(:code:`str`): The path to the input file.
        """
        super().__init__()
        if not os.path.exists(path):
            raise ValueError("Could not find file {}.".format(path))
        self.path = path
        self.file = File(path, mode="r")

    @property
    def n_profiles(self):
        return self.file["C"]["dBZ"].shape[0]

    def get_y_cloudsat(self, i):
        r = self.file["C"]["dBZ"][i][0]
        data = self.file[r][0, :]
        data = np.maximum(data, -30.0)
        return data

    def get_cloudsat_range_bins(self, i):
        r = self.file["C"]["z_field"][i][0]
        z = self.file[r][0, :]
        range_bins = np.zeros(z.size + 1)
        range_bins[1:-1] = 0.5 * (z[1:] + z[:-1])
        range_bins[0] = 2 * range_bins[1] - range_bins[2]
        range_bins[-1] = 2 * range_bins[-2] - range_bins[-3]
        return range_bins

    def get_pressure(self, i):
        r = self.file["C"]["p_grid"][i][0]
        data = self.file[r][0, :]
        return data

    def get_temperature(self, i):
        r = self.file["C"]["t_field"][i][0]
        data = self.file[r][0, :]
        return data

    def get_surface_temperature(self, i):
        r = self.file["C"]["t_surface"][i][0]
        data = self.file[r][0, 0]
        return data

    def get_altitude(self, i):
        r = self.file["C"]["z_field"][i][0]
        data = self.file[r][0, :]
        return data

    def get_H2O(self, i):
        r = self.file["C"]["h2o"][i][0]
        data = self.file[r][0, :]
        return data

    def get_cloud_water(self, i):
        r = self.file["C"]["lwc"][i][0]
        data = self.file[r][0, :]
        return data

    def get_surface_altitude(self, i):
        r = self.file["C"]["z_field"][i][0]
        data = self.file[r][0, 0]
        return data

    def get_surface_wind_speed(self, i):
        r = self.file["C"]["wind_speed"][i][0]
        data = self.file[r][0, :]
        return data

    def get_surface_wind_direction(self, i):
        r = self.file["C"]["wind_dir"][i][0]
        data = self.file[r][0, :]
        return data
