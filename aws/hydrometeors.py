import os

from parts.scattering import ScatteringSpecies
from parts.scattering.psd import D14MN, AB12

try:
    dendrite_path = os.environ["DENDRITE_PATH"]
except:
    home = os.environ["HOME"]
    dendrite_path = os.path.join(home, "Dendrite")

try:
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")
except:
    data_path = os.path.join(".", "..", "data")

shape_names = {
    "6 Bullet Rosette" : "6-BulletRosette",
    "8 Column Aggregate" : "8-ColumnAggregate",
    "Column Type 1" : "ColumnType1",
    "Evans Snow Aggregate" : "EvansSnowAggregate",
    "Float 3 Buller Rosette" : "Flat3-BulletRosette",
    "GEM Graupel" : "GemGraupel",
    "Icon Cloud Ice" : "IconCloudIce",
    "ICON Hail" : "IconHail",
    "ICON Snow" : "IconSnow",
    "Large Block Aggregate" : "LargeBlockAggregate",
    "Large Column Aggregate" : "LargeColumnAggregate",
    "Large Plate Aggregate" : "LargePlateAggregate",
    "Liquid Sphere" : "LiquidSphere",
    "Perpendicular 4 Buller Rosette" : "Perpendicular4-BulletRosette",
    "Plate Type 1" : "PlateType1",
    "Sector Snow Flake" : "SectorSnowflake"}

class D14(D14MN):
    """
    Specialized class implementing a normalized modified gamma distribution
    parametrized using mass density and mass weighted mean diameter (D_m).
    The shape is the same as the one used for the DARDAR v3 retrievals.
    """
    def __init__(self, alpha, beta, rho):
        super().__init__(alpha, beta, rho)
        self.name = "d14"

    @property
    def moment_names(self):
        return ["water_content", "n0"]




class Ice(ScatteringSpecies):
    def __init__(self,
                 shape):
        # PSD, same as DARDAR V3
        alpha = -0.262
        beta = 1.754
        psd = D14(alpha, beta, 917.0)
        psd.t_max = 280.0
        # Look up particle name
        if shape in shape_names:
            name_data = shape_names[shape] + ".xml"
            name_meta = shape_names[shape] + ".meta.xml"
        else:
            raise ValueError("{} is not a known shape. Available shapes are {}".
                             format(shape, shape_names.keys()))

        ssdb_path = os.path.join(dendrite_path,
                                 "SSDB",
                                 "ArtsScatDbase",
                                 "ArtsScatDbase_v1.0.0",
                                 "StandardHabits",
                                 "FullSet")
        scattering_data = os.path.join(data_path, "StandardHabits", name_data)
        scattering_meta_data = os.path.join(ssdb_path, "StandardHabits", name_meta)
        super().__init__("ice", psd, scattering_data, scattering_meta_data)

class Rain(ScatteringSpecies):
    def __init__(self):
        # PSD, same as DARDAR V3
        alpha = 0.0
        beta = 1.0
        psd = D12()
        psd.t_min = 270.0

        ssdb_path = os.path.join(dendrite_path,
                                 "SSDB",
                                 "ArtsScatDbase",
                                 "ArtsScatDbase_v1.0.0",
                                 "StandardHabits",
                                 "FullSet")
        scattering_data = os.path.join(ssdb_path, "LiquidSphere.xml")
        scattering_meta_data = os.path.join(ssdb_path, "LiquidSphere.meta.xml")
        super().__init__("rain", psd, scattering_data, scattering_meta_data)
