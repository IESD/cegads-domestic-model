from cegads import Household
from cegads.appliances import ApplianceFactory

from pkg_resources import resource_filename

path = resource_filename('cegads', 'data/daily profiles.csv')

f = ApplianceFactory(path)

h = Household(
    f('washing_machine'),
    f('dishwasher'),
    f('tumble_dryer')
)

# generate a 7-day, half-hourly time series with events for the timing of usage for each appliance
events = h.simulation(7, 120)

print(events)
