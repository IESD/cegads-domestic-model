from collections import defaultdict
import pandas as pd

from ..exceptions import CEGADSException

class Household(object):
    """a collection of appliances"""
    def __init__(self, *appliances):
        self._names = defaultdict(int)
        self._appliances = {}
        for a in appliances:
            name = self.name_for(a.model.name)
            self._appliances[name] = a

    def appliances(self):
        """return a list of appliances"""
        return self._appliances.values()

    def name_for(self, next_name):
        self._names[next_name] += 1
        return "{}_{}".format(next_name, self._names[next_name])

    def events_as_timeseries(self, days, **kwargs):
        keys = self._appliances.keys()
        if not keys:
            return pd.DataFrame([])
        return pd.concat([self._appliances[key].events_as_timeseries(days, name=key, **kwargs) for key in keys], axis=1, names=keys)

    def simulation(self, days, freq, **kwargs):
        keys = self._appliances.keys()
        if not keys:
            return pd.DataFrame([])
        return pd.concat([self._appliances[key].simulation(days, freq, name=key, **kwargs) for key in keys], axis=1, names=keys)

    def __repr__(self):
        return "Household(\n  {}\n)".format(",\n  ".join([str(a) for a in self.appliances()]))
