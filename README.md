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

Now instantiate an `ApplianceFactory` and use it to create appliances within a household.

```python
f = ApplianceFactory()

h = Household(
    f('washing_machine'),
    f('dishwasher'),
    f('tumble_dryer')
)
```

All similar appliances share the same underlying model object so it is fine to generate large numbers of households in this way.
Now we can use the convenient Household object to simulate a 365-day, half-hourly timeseries.

```python
consumption = h.simulation(365, '30Min')
```
