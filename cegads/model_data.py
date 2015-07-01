from pkg_resources import resource_filename
import os.path

import pandas as pd

from .exceptions import InvalidDataFileError

class ModelData(object):
    """A class to represent model source data
    Can be used to manipulate data before loading it into a model
    """
    def __init__(self, path=None):
        """load data from a file"""
        if not path:
            # Use the default data file unless an alternative file path is provided
            # data source: ECUK table 3.11
            path = resource_filename('cegads', 'data/daily profiles.csv')

        if not os.path.isfile(path):
            raise(InvalidDataFileError("The provided path does not point to a file"))

        df = pd.read_csv(path, parse_dates={'Date': ['Time']})
        df = df.set_index('Date')
        self._data = df

    def total(self, index):
        return self._data[index].sum()

    def profile(self, index, freq, method):
        """Access normalised data interpolated to chosen frequency"""
        s = self._data[index]
        #add midnight to the end
        s[s.index[0] + pd.DateOffset(1)] = s[0]
        #interpolate half hourly slots and return all but the last midnight
        s = s.resample(freq).interpolate(method)[:-1]
        profile = (s / s.sum()).cumsum()
        profile.name = 'profile'
        return profile

    # def half_hourly(self, index, method='linear'):
    #     return self.interpolated(index, '30Min', method)

if __name__ == "__main__":
    import sys
    import os.path
    from matplotlib import pyplot as plt

    args = sys.argv
    if len(args) >= 2:
        print("only one argument - the path to data - is allowed.")
        exit()

    if len(args) == 1:
        path = None
    else:
        path = args[1]
        if not os.path.isfile(path):
            print("cannot find file at {}".format(path))
            exit()


    md = ModelData(path)

# ['Cold Appliances', 'Cooking', 'Lighting', 'Audiovisual', 'ICT', 'Washing/ drying/ dishwasher', 'Water heating', 'Heating', 'Other', 'Unknown', 'Showers']
    index = 'wet_appliances'
    freq = "10Min"
    # ck1 = md.raw('Cooking')
    for method in ['linear', 'cubic', 'quadratic', 'pchip']:
        p = md.profile(index, freq=freq, method=method)
        plt.plot(p.index, p, label=method)
    plt.legend(loc=2)
    plt.savefig("interpolation.png")

    plt.figure(2)
    for key in md._data.keys():
        p = md.profile(key, freq=freq, method='linear')
        plt.plot(p.index, p, label=key)
    plt.legend(loc=2)
    plt.savefig("models.png")
