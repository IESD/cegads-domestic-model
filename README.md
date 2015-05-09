# cegads-domestic-model
An energy consumption model for domestic appliances.

## Usage
The code is very new so nothing is stable yet.
The intention is to allow for the composition of scenarios which are essentially collections of individual households.
Households are in turn collections of appliance models.

My first stab at an interface looks like this:

First, import the Household class and ApplianceFactory from the cegads library.

```python
from cegads import Household
from cegads.appliances import ApplianceFactory
```

Then get the path to included data file using pkg_resources.

```python
from pkg_resources import resource_filename
path = resource_filename('cegads', 'data/daily profiles.csv')
```

Now instantiate an `ApplianceFactory` with the data file and use it to create appliance models.
note: the factory should generate singleton instances of model objects but does not yet do so.

```python
f = ApplianceFactory(path)

h = Household(
    f('washing_machine'),
    f('dishwasher'),
    f('tumble_dryer')
)
```

Now we can use the convenient Household object to generate a dataset of events.

```python
events = h.events_as_timeseries(7)
```

This generates a 7-day, half-hourly time series with events for the timing of usage for each appliance.
This is not the same as a full simulation. Simulation will include power and cycle duration and is coming soon.
