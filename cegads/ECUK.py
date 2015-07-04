from pkg_resources import resource_filename
import pandas as pd

from .exceptions import InvalidYearError, InvalidDeviceError

__all__ = ["ECUK"]

class ECUK(object):
    """wrap the ECUK data in a nice convenient interface"""
    def __init__(self):
        table_3_08_path = resource_filename('cegads', 'data/number_of_households.csv')
        table_3_10_path = resource_filename('cegads', 'data/ECUK Table 3.10.csv')
        table_3_12_path = resource_filename('cegads', 'data/number_of_appliances.csv')
        profile_path = resource_filename('cegads', 'data/daily profiles.csv')

        table_3_08 = pd.read_csv(table_3_08_path).set_index('year')['households'] * 1000

        table_3_10 = pd.read_csv(table_3_10_path, skiprows=1, index_col=0) * 11630000000 # convert to Wh
        table_3_10.columns.name = "device"
        table_3_10 = table_3_10.stack()
        table_3_10.name = 'annual consumption'

        table_3_12 = pd.read_csv(table_3_12_path, skiprows=1, index_col=0).astype(int) * 1000
        table_3_12.columns.name = "device"
        table_3_12 = table_3_12.stack()
        table_3_12.name = 'appliances'

        self._data = pd.DataFrame(table_3_12).join(table_3_10).join(table_3_08)
        self._data['consumption_per_appliance'] = self._data['annual consumption'] / self._data['appliances']
        self._data['appliances_per_household'] = self._data['appliances'] / self._data['households']
        self._data = self._data.stack().unstack(level=0)

    def __getitem__(self, year):
        return self._data[year].unstack()

    def __call__(self, year, device=None):
        try:
            df = self._data[year].unstack()
        except KeyError:
            raise InvalidYearError("Year {} not found".format(year))
        if device:
            search = df.index==device
            if not search.any():
                raise InvalidDeviceError("Device '{}' not found".format(device))
            return df[search].squeeze()

        else:
            return df

    def consumption(self, year):
        indexer = [slice(None)]*len(self.table_3_10.index.names)
        indexer[self.table_3_10.index.names.index('Year')] = year
        return self.table_3_10.loc[tuple(indexer)]

    def appliances_per_household(self, year):
        indexer = [slice(None)]*len(self.table_3_12.index.names)
        indexer[self.table_3_12.index.names.index('Year')] = year
        apps = self.table_3_12.loc[tuple(indexer)] / self.table_3_08


    def consumption_per_appliance(self, year):
        indexer = [slice(None)]*len(self.table_3_10.index.names)
        indexer[self.table_3_10.index.names.index('Year')] = year
        cons = self.table_3_10.loc[tuple(indexer)]
        apps = self.table_3_12.loc[tuple(indexer)]
        # df = pd.DataFrame([apps, cons])
        # return df['WET']
        result = (cons / apps)
        result.name = "appliances per household"
        return result
