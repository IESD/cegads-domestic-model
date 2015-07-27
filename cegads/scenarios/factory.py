# from pkg_resources import resource_filename
import os.path

import pandas as pd

from ..ECUK import ECUK
from ..appliances.factory import ApplianceFactory
from ..scenarios.scenario import Scenario

class ScenarioFactory(ECUK):
    """Scenario factory can generate scenario objects for a given year"""

    def __init__(self, appliance_factory=None):
        super(ScenarioFactory, self).__init__()
        self.appliance_factory = appliance_factory or ApplianceFactory()

    def __call__(self, year):
        data = super(ScenarioFactory, self).__call__(year)
        return Scenario(self.appliance_factory, data)
