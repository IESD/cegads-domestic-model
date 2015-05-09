import numpy as np
import pandas as pd
import datetime

from .model_data import ModelData
from . import CEGADSException

class Appliance(object):
    def __init__(self, data):
        self.name = data.name
        self.data = (data / data.sum()).cumsum()
        # make an index from the data
        self.lookup = pd.Index(self.data)

    def events(self, days):
        """return a simple list of events, drawn from the model"""
        # generate some randomness
        seed = np.random.random(days)
        # find the index where each random number would fit
        i = self.lookup.searchsorted(seed) # can use side='left' or side='right'
        raw_events = self.data.index[i]     # 7 values, all in the same day
        # spread them over different days
        raw_events = pd.Index([(rt + datetime.timedelta(days=j)) for j, rt in enumerate(raw_events)])
        return raw_events


    def events_as_timeseries(self, days):
        """combine raw events into a complete time series"""
        raw_events = self.events(days)
        # generate a daily index covering the period (including following midnight)
        index = pd.DatetimeIndex(pd.date_range(start=raw_events[0].date(), freq='D', periods=days+1))
        # expand into a half hourly dataset and knock the last one off (the extra midnight)
        result = pd.Series(index=index, name=self.name).resample('30Min')[:-1]
        # set the data to false, overwrite our events with true
        result[:] = False
        result[raw_events] = True
        return result

    def simulation(self, days):
        raise NotImplementedError

supported_appliances = set([
    'washing_machine',
    'dishwasher',
    'tumble_dryer'
])

mapping = {
    'washing_machine': 'wet_appliances',
    'dishwasher': 'wet_appliances',
    'tumble_dryer': 'wet_appliances'
}

class UnsupportedAppliance(CEGADSException): pass

class ApplianceFactory(object):
    def __init__(self, path):
        self.md = ModelData(path)

    def __call__(self, appliance):
        if appliance not in supported_appliances:
            raise UnsupportedAppliance("{} not supported, try one of {}".format(appliance, ','.join(supported_appliances.keys())))
        data = self.md.half_hourly(mapping[appliance])
        data.name = appliance
        return Appliance(data)
