from h5py import File

class Profiles:
    """
    Data provider class that provides the parts interface for an
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
        self.path = path
        self.file = File(path)

    def get_y_cloudsat(self, i):
        r = self.file["C"]["dBZ"][i][0]
        data = self.file[r][0, :]
        return data

    def get_pressure(self, i):
        r = self.file["C"]["p_grid"][i][0]
        data = self.file[r][0, :]
        return data

    def get_temperature(self, i):
        r = self.file["C"]["t_field"][i][0]
        data = self.file[r][0, :]
        return data

    def get_temperature(self, i):
        r = self.file["C"]["t_field"][i][0]
        data = self.file[r][0, :]
        return data

    def get_altitude(self, i):
        r = self.file["C"]["z_field"][i][0]
        data = self.file[r][0, :]
        return data

    def get_H2O(self, i):
        r = self.file["C"]["h2o"][i][0]
        data = self.file[r][0, :]
        return data

    def get_lwc(self, i):
        r = self.file["C"]["lwc"][i][0]
        data = self.file[r][0, :]
        return data

    def get_surface_altitude(self, i):
        r = self.file["C"]["z_surface"][i][0]
        data = self.file[r][0, :]
        return data

    def get_surface_wind_speed(self, i):
        r = self.file["C"]["wind_speed"][i][0]
        data = self.file[r][0, :]
        return data

    def get_surface_wind_direction(self, i):
        r = self.file["C"]["wind_dir"][i][0]
        data = self.file[r][0, :]
        return data
