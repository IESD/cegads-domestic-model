import numpy as np
import pandas as pd
import datetime

from ..model_data import ModelData
from .. import CEGADSException

class UnsupportedAppliance(CEGADSException): pass

# mapping between allowed API appliance names and columns in data file
mapping = {
    'washing_machine': 'wet_appliances',
    'dishwasher': 'wet_appliances',
    'tumble_dryer': 'wet_appliances'
}

class ApplianceModel(object):
    """The base appliance model
    Eats a consumption profile (one day) and a total daily consumption value
    serves up randomised simulated usage over any period
    """
    def __init__(self, profile, daily_total, name, freq):
        self.freq = freq
        self.name = name
        self.daily_total = daily_total
        self.profile = profile
        # make an index from the data
        self.lookup = pd.Index(self.profile)

    def events(self, days, start=None, random_data=None):
        """return a simple list of events, drawn from the model"""
        if not random_data:
            # generate some randomness
            random_data = np.random.random(days)

        if not start:
            start = datetime.date.today()

        # find the index where each random number would fit
        # I think the random number is <1 so side='right' should be good
        i = self.lookup.searchsorted(random_data, side='right')
        raw_events = pd.DataFrame(self.profile.index[i].time, columns=['time'])     # get the times

        # create a date range for the events
        raw_events['date'] = pd.date_range(start=start, periods=days)

        # combine the date and times via formatting as strings, combining and parsing
        raw_events['date_string'] = raw_events['date'].apply(lambda x: x.strftime('%d-%m-%Y '))
        raw_events['time_string'] = raw_events['time'].apply(lambda x: x.strftime('%H:%M'))
        raw_events['datetime_string'] = raw_events.apply(lambda x: x.date_string + x.time_string, axis=1)
        raw_events['datetime'] = raw_events.apply(lambda x: datetime.datetime.strptime(x.date_string + x.time_string, '%d-%m-%Y %H:%M'), axis=1)
        return pd.Index(raw_events['datetime'])



    def events_as_timeseries(self, days):
        """combine raw events into a complete time series"""
        raw_events = self.events(days)
        # generate a daily index covering the period (including following midnight)
        index = pd.DatetimeIndex(pd.date_range(start=raw_events[0].date(), freq='D', periods=days+1))
        # expand into a half hourly dataset and knock the last one off (the extra midnight)
        result = pd.Series(index=index, name=self.name).resample(self.freq)[:-1]
        # set the data to false, overwrite our events with true
        result[:] = False
        result[raw_events] = True
        return result

    def simulation(self, days, cycle_length, freq):
        """given a cycle length, simulates actual consumption values at a given resolution"""
        events = self.events_as_timeseries(days)
        result = events
        point_value = self.daily_total / cycle_length
        for i in range(cycle_length):   # In python 2 this generates a list - a (small?) waste of memory
            delta = i - int(float(cycle_length)/2)
            result = result | events.shift(delta)
        result = (result * point_value).resample(freq, how="sum")
        return result


class ModelFactory(object):
    """a source of models
    generates reusable models from model data in a file at path
    frequency and interpolation method can be specified
    """

    def __init__(self, path, freq, method):
        self.freq = freq
        self.method = method
        self.md = ModelData(path)
        self.models = {}

    def __call__(self, appliance):
        if appliance not in self.models.keys():
            try:
                mapped_name = mapping[appliance]
            except KeyError:
                raise UnsupportedAppliance("{} not supported, try one of {}".format(appliance, ','.join(mapping.keys())))
            self._load_model(appliance, mapped_name)    # generates a new model
        return self.models[appliance]

    def _load_model(self, appliance, mapped_name):
        profile = self.md.profile(mapped_name, self.freq, self.method)
        total = self.md.total(mapped_name)
        self.models[appliance] = ApplianceModel(profile, total, appliance, self.freq)
        # return self.models[mapped_name]
