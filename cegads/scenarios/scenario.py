from pkg_resources import resource_filename
import os.path
from random import random

from ..exceptions import InvalidDataFileError, UnsupportedAppliance
from ..households import Household

class Scenario(object):
    """scenarios determine the probability of households owning each type of appliance
    It acts much like a HouseholdFactory"""

    def __init__(self, appliance_factory, data):
        self._data = data
        self.appliance_factory = appliance_factory

    def __getattr__(self, name):
        return getattr(self._data, name)

    def household(self, requested_appliances):
        """generate a household with the requested appliances"""
        appliances = []
        for appliance, cycle_length in requested_appliances:
            appliance_filter = self._data.index==appliance
            if not appliance_filter.any():
                raise UnsupportedAppliance("This scenario doesn't include ownership data for the requested appliance '{}'".format(appliance))
            app_data = self._data[appliance_filter].squeeze()
            per_household = app_data.appliances_per_household
            daily_consumption = app_data.consumption_per_appliance / 365
            while per_household > 0:
                if random() <= per_household:
                    a = self.appliance_factory(appliance, cycle_length, daily_consumption)
                    appliances.append(a)
                per_household -= 1
        return Household(*appliances)

    def appliance(self, appliance, cycle_length):
        try:
            app_data = self._data[self._data.index==appliance].squeeze()
        except KeyError:
            raise UnsupportedAppliance("This scenario doesn't include ownership data for the requested appliance '{}'".format(appliance))
        daily_consumption = app_data.consumption_per_appliance / 365
        return self.appliance_factory(appliance, cycle_length, daily_consumption)
