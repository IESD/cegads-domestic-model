from pkg_resources import resource_filename
import os.path

import pandas as pd

from ..exceptions import InvalidDataFileError, ScenarioNotFound, InvalidYearError
from ..appliances.factory import ApplianceFactory
from ..scenarios.scenario import Scenario

class ScenarioFactory(object):
    """Scenario factory loads data and can generate scenario objects for a given year"""

    def __init__(self, appliance_factory=None, appliance_path=None, household_path=None):
        if not appliance_path: # data source: ECUK table 3.12
            appliance_path = resource_filename('cegads', 'data/number_of_appliances.csv')

        if not household_path: # data source: ECUK table 3.08
            household_path = resource_filename('cegads', 'data/number_of_households.csv')

        if not os.path.isfile(appliance_path):
            raise(InvalidDataFileError("The provided path does not point to a file"))

        if not os.path.isfile(household_path):
            raise(InvalidDataFileError("The provided path does not point to a file"))

        appliances = pd.read_csv(appliance_path).set_index('Year')
        households = pd.read_csv(household_path).set_index('Year')['Households']
        self._data = appliances.div(households, axis=0)
        if not appliance_factory:
            appliance_factory = ApplianceFactory()
        self.appliance_factory = appliance_factory

    def __call__(self, year):
        try:
            data = self._data[self._data.index == year].squeeze()
        except KeyError:
            raise InvalidYearError("Invalid year '{}' provided".format(year))
        else:
            if data.empty:
                raise ScenarioNotFound("No scenario found for year '{}'".format(year))

        return Scenario(self.appliance_factory, data)
