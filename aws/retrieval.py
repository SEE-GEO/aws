from aws.simulation import Simulation
from aws.sensor import CloudSat
from parts.jacobian import Log10

class RainAPriori:
    def __init__(self):
        pass

    def get_rain_a_priori(self, *args, **kwargs):
        t = self.owner.get_altitude(*args, **kwargs)
        xa = np.zeros(t.shape)
        xa[:] = 1e-6
        xa[t < 273.15] = 1e-12
        return np.log10(xa)

    def get_rain_covariance(self, *args, **kwargs):
        t = self.owner.get_altitude(*args, **kwargs)
        covmat = np.diag(2.0 * np.ones(t.size))
        return covmat

    def get_rain_n0(self, *args, **kwargs):
        return 1e7

class IceAPriori:
    def __init__(self):
        pass

    def get_ice_a_priori(self, *args, **kwargs):
        t = self.owner.get_altitude(*args, **kwargs)
        xa = np.zeros(t.shape)
        xa[:] = 1e-6
        xa[t > 273.15] = 1e-12
        return np.log10(xa)

    def get_ice_covariance(self, *args, **kwargs):
        t = self.owner.get_altitude(*args, **kwargs)
        covmat = np.diag(2.0 * np.ones(t.size))
        return covmat

    def get_ice_n0(self, *args, **kwargs):
        t = self.owner.get_altitude(*args, **kwargs)
        return np.log10(np.exp(-0.076586 * t + 17.948))

class Retrieval(Simulation):
    def __init__(self,
                 data_provider,
                 ice_shape = "8 Column Aggregate"):
        sensor = CloudSat()
        super().__init__(sensor,
                         data_provider,
                         ice_shape=ice_shape)

        scatterers = self.atmosphere.scatterers
        # Add first moment ice to retrieval and set transform
        ice = [s for s in scatterers if s.name == "ice"][0]
        self.retrieval.add(ice.moments[0])
        ice.transformation = Log10()

        # Add first moment of rain PSD to retrieval and set transform
        rain = [s for s in scatterers if s.name == "rain"][0]
        self.retrieval.add(rain.moments[0])
        rain.transformation = Log10()






