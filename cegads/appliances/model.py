import numpy as np
import pandas as pd
import datetime

from ..model_data import ModelData
from ..exceptions import UnsupportedAppliance

# mapping between allowed API appliance names and columns in data file
mapping = {
    'Standard Light Bulb': 'Lighting',
    'Halogen': 'Lighting',
    'Fluorescent Strip Lighting': 'Lighting',
    'Energy Saving Light Bulb': 'Lighting',
    'LED': 'Lighting',
    'Chest Freezer': 'Cold Appliances',
    'Fridge-freezer': 'Cold Appliances',
    'Refrigerator': 'Cold Appliances',
    'Upright Freezer': 'Cold Appliances',
    'Washing Machine': 'wet_appliances',
    'Washer-dryer': 'wet_appliances',
    'Dishwasher': 'wet_appliances',
    'Tumble Dryer': 'wet_appliances',
    'TV': 'Audiovisual',
    'Set Top Box': 'Audiovisual',
    'DVD/VCR': 'Audiovisual',
    'Games Consoles': 'Audiovisual',
    'Power Supply Units': 'Audiovisual',
    'Desktops': 'ICT',
    'Laptops': 'ICT',
    'Monitors': 'ICT',
    'Printers': 'ICT',
    'Multi-Function Devices': 'ICT',
    'Electric Oven': 'Cooking',
    'Electric Hob': 'Cooking',
    'Microwave': 'Cooking',
    'Kettle': 'Cooking',
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

    def events(self, days, profile=None, start=None, random_data=None, name=None):
        """return a simple list of events, drawn from the model"""
        if profile is not None:
            lookup = pd.Index(profile)
        else:
            lookup = self.lookup
            profile = self.profile

        if not start:
            start = datetime.datetime.now()

        if not random_data:
            # generate some randomness
            random_data = np.random.random(days)

        if not name:
            name = self.name
        # find the index where each random number would fit
        # I think the random number is <1 so side='right' should be good
        indices = lookup.searchsorted(random_data, side='right')
        # add a series of days onto the dates
        dates = pd.Series(profile.index[indices]) + pd.to_timedelta(np.arange(len(indices)), unit='d')
        dates = pd.Index(dates, name=name).to_datetime()
        return dates.shift(1, start.replace(microsecond=0, second=0, minute=0, hour=0) - dates[0].replace(microsecond=0, second=0, minute=0, hour=0))


    def simulation(self, days, cycle_length, freq, **kwargs):
        """given a cycle length, simulates actual consumption values at a given resolution"""
        events = self.events(days, **kwargs)
        # create a constant timestep series covering the whole period
        start = events[0].date()
        end = start + datetime.timedelta(days=days) # This creates an extra row
        result = pd.Series(0,
            index=pd.date_range(start=start, end=end, freq=self.freq),
            name=events.name
        )[:-1] # remove last row here

        # construct an index into all the minutely timesteps in which the appliance is ON
        index = pd.DatetimeIndex(
            pd.Series(events.repeat(cycle_length)) + pd.to_timedelta(np.tile(((np.arange(cycle_length)-int(cycle_length/2))*60), days), unit="s")
        ).intersection(result.index)

        # set the matching values to the minutely consumption (total/cycle_length)
        result[index] = self.daily_total / cycle_length
        result = result.resample(freq, how="sum")
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

    def appliance_keys(self):
        return set(mapping.keys()) | set(mapping.values())

    def __call__(self, appliance, daily_consumption=None):
        if appliance not in self.models.keys():
            try:
                mapped_name = mapping[appliance]
            except KeyError:
                mapped_name = appliance
            self._load_model(appliance, mapped_name, daily_consumption)    # generates a new model
        return self.models[(appliance, daily_consumption)]

    def _load_model(self, appliance, mapped_name, daily_consumption):
        profile = self.md.profile(mapped_name, self.freq, self.method)
        total = daily_consumption or self.md.total(mapped_name)
        self.models[(appliance, daily_consumption)] = ApplianceModel(profile, total, appliance, self.freq)
