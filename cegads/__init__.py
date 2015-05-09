import pandas as pd

class CEGADSException(Exception): pass

class Household(object):
    """a collection of appliances"""
    def __init__(self, *appliances):
        self.appliances = appliances

    def events_as_timeseries(self, days):
        return pd.concat([a.events_as_timeseries(days) for a in self.appliances], axis=1)

    def simulation(self, days):
        return pd.concat([a.simulation(days) for a in self.appliances], axis=1)
