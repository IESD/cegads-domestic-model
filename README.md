# cegads-domestic-model
This library implements a simple domestic appliance model based on data from chapter three of the DECC ECUK publication (https://www.gov.uk/government/collections/energy-consumption-in-the-uk). and provides a convenient interface for generating household simulations at the appliance level.

## Installation

`pip install` **`[--upgrade]`** `cegads-domestic-model`

or visit the [github repo](http://www.github.com/IESD/cegads-domestic-model) and download the code.

The implementation is based on [`pandas`](http://pandas.pydata.org/) so you will need to install that before it will work.

## Usage
The intention is to allow for the easy generation of households which are collections of appliance models. Households are generated via scenarios which are aware of the national statistics for appliance ownership (a scenario represents a specific year from the data). Appliances are aware of the overall daily profile data and total annual consumption for the given scenario year.

The code is becoming stable but we are still in the early development phase so the interface is subject to change.

A more detailed review of the library can be found [here](https://github.com/IESD/cegads-domestic-model/blob/master/cegads/examples/Basic%20usage.ipynb)

###Initialisation
First, create an instance of the ScenarioFactory class. This class has access to the full ECUK dataset.

```python
from cegads import ScenarioFactory
factory = ScenarioFactory()
```

Now we can create a scenario for any year available in the data. Here I have chosen 2013.

```python
# load data for 2013
scenario = factory(2013)
```

Scenario instances can be used to generate appliances (using `scenario.appliance()`)
and households (using `scenario.household()`).


### Simulating appliances

Creating appliances requires an appliance key to identify the type of appliance to create and a duty cycle (in minutes).
A full list of available appliance keys can be accessed using the `scenario.appliance_keys()` method.
The duty_cycle parameter determines how long the appliance operates for each day.
The timing of the operation is determined by the model.

```python
# create a Washing Machine with an 80-minute duty cycle
washing_machine = scenario.appliance('Washing Machine', 80)
```

Actual simulation data can be generated directly from Appliance instances using the `Appliance.simulation()` method.
It takes two required parameters, the number of days to simulate and the frequency in which to output the result.
The model runs at minutely resolution by default so the frequency parameter simply aggregates the minutely simulation data.
The method also takes keyword arguments. Here I have set the start date of the simulated output to a python datetime object.

```python
from datetime import datetime
start = datetime(2013, 1, 1)
# a 365-day simulation at 30-minute resolution
result = washing_machine.simulation(365, "30Min", start=start)
```

The output of the simulation is a pandas Series with a datetime index.

### Simulating households

Scenario objects have access to ECUK statistics about appliance ownership. This makes creating a collection of households with the appropriate allocation of appliances easy.

The `scenario.household()` method takes a list of appliances to consider as its only argument. The list must contain (appliance_key, duty_cycle) two-tuples. Each appliance passed in the list will be considered for inclusion in the household based on ECUK appliance ownership data. For example, if the appliance ownership is 50% then there will be a 50% chance of the appliance being allocated to the generated household.

```python
appliances_to_consider = [
    ('Washing Machine', 80),
    ('Dishwasher', 100),
    ('Tumble Dryer', 120),
    ('Washer-dryer', 180)
]
household = scenario.household(appliances_to_consider)
```

Household object have a convenient wrapper function which aggregates the individual appliance simulation results into one dataframe.

```python
result = household.simuation(365, "30Min", start=start)
```

Large collections of households can be easily generated in a similar way.

```python
households = [scenario.household(appliances_to_consider) for i in range(150)]
```
