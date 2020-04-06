import numpy as np
import os

import os

from aws.retrieval import Simulation, Retrieval
from aws.data import Profiles
from aws.sensor import AWS, band_166, band_183l, band_229, band_325l, band_325u
from aws.retrieval import Retrieval
from aws.data import Profiles

try:
    from IPython import get_ipython
    ip = get_ipython()
    ip.magic("%load_ext autoreload")
    ip.magic("%autoreload 2")
except:
    pass

try:
    path = os.path.dirname(__file__)
except:
    path = "."

data_provider = Profiles(os.path.join(path, "..", "data", "testdata.mat"))

# Create the retrieval and let it act as data provider to simulations.
retrieval = Retrieval(data_provider, "Perpendicular3BulletRosette")
data_provider.add(retrieval)


# Simulation
frequencies = np.concatenate([band_166,
                              band_183l,
                              band_229,
                              band_325l,
                              band_325u])
sensor = AWS(frequencies)
simulation = Simulation(sensor, data_provider, "Perpendicular3BulletRosette")
simulation.setup()
simulation.run(0)
