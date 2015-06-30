from collections import defaultdict
import pandas as pd

from .exceptions import CEGADSException

class Household(object):
    """a collection of appliances"""
    def __init__(self, *appliances):
        self._names = defaultdict(int)
        self.appliances = {}
        for a in appliances:
            name = self.name_for(a.model.name)
            self.appliances[name] = a

    def name_for(self, next_name):
        self._names[next_name] += 1
        return "{}_{}".format(next_name, self._names[next_name])

    def events_as_timeseries(self, days, **kwargs):
        keys = self.appliances.keys()
        return pd.concat([self.appliances[key].events_as_timeseries(days, name=key, **kwargs) for key in keys], axis=1, names=keys)

    def simulation(self, days, freq, **kwargs):
        keys = self.appliances.keys()
        return pd.concat([self.appliances[key].simulation(days, freq, name=key, **kwargs) for key in keys], axis=1, names=keys)
