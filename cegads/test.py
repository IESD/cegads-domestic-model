from cegads import Household
from cegads.appliances import ApplianceFactory

from pkg_resources import resource_filename

path = resource_filename('cegads', 'data/daily profiles.csv')

f = ApplianceFactory(path)

h = Household(
    f('washing_machine', 240),
    f('dishwasher', 60),
    f('tumble_dryer', 120)
)

# generate a 7-day, half-hourly time series of consumption for each appliance
consumption = h.simulation(365, '30Min')

consumption.to_csv("example_data.csv")
