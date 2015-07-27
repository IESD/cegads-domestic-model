import unittest

from cegads import (
    Household,
    ScenarioFactory,
    InvalidDataFileError,
    InvalidYearError,
    CEGADSException
)

valid_year = 2013
valid_appliances = [
    ('Washing Machine', 20),
    ('Dishwasher', 20),
    ('Tumble Dryer', 20),
]

class TestScenario(unittest.TestCase):
    def setUp(self):
        sf = ScenarioFactory()
        self.sc = sf(valid_year)

    def test_household_ok(self):
        try:
            h = self.sc.household(valid_appliances)
        except CEGADSException as e:
            self.fail("getting household '{}' raised {} unexpectedly!".format(valid_appliances, e.__class__.__name__))
        self.assertIsInstance(h, Household)


if __name__ == "__main__":
    unittest.main()
