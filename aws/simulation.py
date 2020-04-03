import os

from artssat import ArtsSimulation
from artssat.atmosphere import Atmosphere1D
from artssat.atmosphere.absorption import H2O, CloudWater, O2, N2
from artssat.atmosphere.surface import Tessem
from artssat.scattering.solvers import RT4
from artssat.atmosphere.catalogs import LineCatalog
from pyarts.workspace.api import include_path_push

from aws.hydrometeors import Ice, Rain
from aws.sensor import AWS

try:
    aws_path = os.path.dirname(__file__)
except:
    aws_path = "."
include_path_push(os.path.join(aws_path, "include"))


class Simulation(ArtsSimulation):
    def __init__(self,
                 sensor,
                 data_provider,
                 ice_shape = "8-Column-Aggregate"):
        scatterers = [Ice(ice_shape), Rain()]
        absorbers = [H2O(), CloudWater()]
        surface = Tessem()
        scattering_solver = RT4(nstreams=32)
        atmosphere = Atmosphere1D(absorbers=absorbers,
                                  scatterers=scatterers,
                                  surface=surface,
                                  catalog=LineCatalog("abs_lines_h2o_rttov.xml"))


        self.includes = ["general/general.arts",
                         "include_mpm89_cont.arts",
                         "general/planet_earth.arts"]

        super().__init__(atmosphere=atmosphere,
                         data_provider=data_provider,
                         sensors=[sensor],
                         scattering_solver=scattering_solver)
