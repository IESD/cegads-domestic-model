import unittest
import datetime
from cegads.appliances.model import ModelFactory, UnsupportedAppliance, ApplianceModel

valid_appliance = 'washing_machine'
invalid_appliance = 'invalid_appliance'

class TestModelFactory(unittest.TestCase):
    def setUp(self):
        self.mf = ModelFactory(None, "10Min", "linear")

    def test_raises_on_invalid_appliance(self):
        self.assertRaises(UnsupportedAppliance, self.mf, invalid_appliance)

    def test_ok_on_valid_appliance(self):
        try:
            model = self.mf(valid_appliance)
        except UnsupportedAppliance:
            self.fail("getting a {} raised UnsupportedAppliance unexpectedly!".format(valid_appliance))
        self.assertIsInstance(model, ApplianceModel)


class TestApplianceModel(unittest.TestCase):
    def setUp(self):
        self.factory = ModelFactory(None, "10Min", "linear")
        self.appliance = self.factory(valid_appliance)

    def test_midnight_events(self):
        """passing in zeros should produce events at midnight"""
        days = 30
        events = self.appliance.events(days, start=datetime.datetime(2001, 1, 1), random_data=[0]*days)
        self.assertTrue((events.hour == 0).all())
        self.assertTrue((events.day == range(1, days+1)).all())

if __name__ == "__main__":
    unittest.main()
