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

df = consumption.groupby(consumption.index.time).sum()

from matplotlib import pyplot as plt

plt.plot(df.index, df)
plt.xlabel("time of day")
plt.ylabel("average consumption (Wh)")
# plt.tight_layout()
# plt.autoscale(axis='x')
plt.savefig("tentatively_testing.png", dpi=600)
