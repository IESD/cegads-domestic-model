import logging
from datetime import datetime

from matplotlib import pyplot as plt

from cegads import ScenarioFactory

log = logging.getLogger()

logging.basicConfig(level=logging.DEBUG)

factory = ScenarioFactory()

scenario = factory(2013)

appliances = [
    ('washing_machine', 60),
    ('dishwasher', 60),
    ('tumble_dryer', 60),
    ('washer_dryer', 60)
]

households = [scenario.household(appliances) for i in range(10)]

f = plt.figure()
for i, h in enumerate(households):
    lbl = "household_{}".format(i)
    log.info("simulating {}".format(lbl))
    sim = h.simulation(365, '10Min', start=datetime(2013, 1, 1))  # half hourly simulation for one year
    if sim.empty:
        continue
    profile = sim.sum(axis=1).groupby(sim.index.time).mean()
    # total = sim.sum(axis=1)
    plt.plot(profile.index, profile, label=lbl)
    plt.legend(prop={'size':6})
plt.savefig("scenario_example", dpi=300)
