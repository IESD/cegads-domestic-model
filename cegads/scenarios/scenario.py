from pkg_resources import resource_filename
import os.path
from random import random

from ..exceptions import InvalidDataFileError, UnsupportedAppliance
from ..households import Household

class Scenario(object):
    """scenarios determine the probability of households owning each type of appliance"""

    def __init__(self, appliance_factory, data):
        self._data = data
        self._households = []
        self.appliance_factory = appliance_factory

    def household(self, requested_appliances):
        """generate a household with the requested appliances"""
        appliances = []
        for appliance, cycle_length in requested_appliances:
            per_household = self._data[appliance]
            if not per_household:
                raise UnsupportedAppliance("This scenario doesn't include ownership data for the requested appliance [{}]".format(appliance))
            while per_household > 0:
                if random() <= per_household:
                    a = self.appliance_factory(appliance, cycle_length)
                    appliances.append(a)
                per_household -= 1
        return Household(*appliances)
