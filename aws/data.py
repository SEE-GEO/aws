import os
import numpy as np
import re
import glob
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

    def get_temperature_field(self):
        t = []
        for i in range(self.n_profiles):
            t += [self.get_temperature(i)]
        return np.stack(t)

    def get_surface_temperature(self, i):
        r = self.file["C"]["t_surface"][i][0]
        data = self.file[r][0, 0]
        return data

    def get_altitude(self, i):
        r = self.file["C"]["z_field"][i][0]
        data = self.file[r][0, :]
        return data

    def get_altitude_field(self):
        z = []
        for i in range(self.n_profiles):
            z += [self.get_altitude(i)]
        return np.stack(z)

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

    def get_latitude(self, i):
        r = self.file["C"]["lat"][i][0]
        data = self.file[r][0, :]
        return data

    def get_latitudes(self):
        lat = []
        for i in range(self.n_profiles):
            lat += [self.get_latitude(i)]
        return np.stack(lat)

    def get_longitude(self, i):
        r = self.file["C"]["lon"][i][0]
        data = self.file[r][0, :]
        return data

    def get_ice_water_content_field(self):
        iwc = []
        for i in range(self.n_profiles):
            r = self.file["C"]["iwc"][i][0]
            iwc += [self.file[r][0, :]]
        return np.stack(iwc)

    def get_rain_water_content_field(self):
        iwc = []
        for i in range(self.n_profiles):
            r = self.file["C"]["rwc"][i][0]
            iwc += [self.file[r][0, :]]
        return np.stack(iwc)

pattern = re.compile(".*c_of_[\d]*_[\d]*_[\d]*.mat")

class RandomProfile(DataProviderBase):
    """
    Data provider returning a random profile from a folder of orbit files.

    Attributes:
        self.path: The folder containing the input orbits.
    """
    def __init__(self, path):
        """
        """
        super().__init__()
        files = glob.glob(os.path.join(path, "*.mat"))
        self.files = [f for f in files if pattern.match(f)]

        def make_getter(name):
            def getter(self, *args, **kwargs):
                profiles = self._get_random_file()
                index = self._get_random_index(profiles)
                fget = getattr(profiles, "get_" + name)
                return fget(index)
            return getter

        getters = ["y_cloudsat",
                   "cloudsat_range_bins",
                   "pressure",
                   "temperature",
                   "surface_temperature",
                   "altitude",
                   "H2O",
                   "cloud_water",
                   "surface_altitude",
                   "surface_windspeed",
                   "surface_wind_direction",
                   "latitude",
                   "longitude"]

        for g in getters:
            self.__dict__["get_" + g] = make_getter(g).__get__(self)

    def _get_random_file(self):
        return Profiles(self.files[np.random.randint(len(self.files))])

    def _get_random_index(self, profiles):
        return np.random.randint(profiles.n_profiles)
