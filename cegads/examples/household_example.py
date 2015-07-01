from matplotlib import pyplot as plt

from cegads import Household
from cegads.appliances import ApplianceFactory

f = ApplianceFactory()

h = Household(
    f('washing_machine', 10),
    f('dishwasher', 5),
    f('dishwasher', 15),
    f('tumble_dryer', 20),
    f('Water heating', 20),
)

# use another model to create a profile
another_profile = f.model_factory('Water heating').profile

# generate a 365-day, half-hourly time series of consumption for each appliance
consumption1 = h.simulation(365, '30Min')
consumption2 = h.simulation(365, '30Min', profile=another_profile)

consumption1.to_csv("example_data.csv")

df1 = consumption1.groupby(consumption1.index.time).sum()
df2 = consumption2.groupby(consumption2.index.time).sum()



for key in sorted(df1.columns):
    plt.plot(df1.index, df1[key], label=df1[key].name, color="red")
for key in sorted(df2.columns):
    plt.plot(df2.index, df2[key], label="adjusted_{}".format(df2[key].name), color="blue")

plt.xlabel("time of day")
plt.ylabel("average consumption (Wh)")
plt.legend()
plt.savefig("tentatively_testing.png", dpi=600)
