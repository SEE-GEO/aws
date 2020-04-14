import numpy as np
import os

import os

from aws.retrieval import Simulation, Retrieval
from aws.sensor import ATMS
from aws.retrieval import Retrieval
from aws.data import RandomProfile

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

data_provider = RandomProfile("/home/simonpf/Dendrite/Projects/AWS-325GHz/CasesV1")
data_provider_2 = RandomProfile("/home/simonpf/Dendrite/Projects/AWS-325GHz/CasesV1")

# Create the retrieval and let it act as data provider to simulations.
retrieval = Retrieval(data_provider, "Perpendicular3BulletRosette")
retrieval.add(data_provider)

sensor = ATMS()
simulation = Simulation(sensor, data_provider, "Perpendicular3BulletRosette")
#simulation.setup()
#simulation.run(28)

import dill
dill.dump(simulation, open("sim.pckl", "wb"))

for i in range(100):
    print(i)
    sim = dill.load(open("sim.pckl", "rb"))
    sim.data_provider = None
