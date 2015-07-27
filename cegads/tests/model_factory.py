import unittest
import datetime

import numpy as np

from cegads.appliances.model import ModelFactory, UnsupportedAppliance, ApplianceModel

valid_appliance = 'Washing Machine'
invalid_appliance = 'invalid_appliance'

# just some random numbers to seed the simulation
seed = [ 0.28190211,  0.14322136,  0.66798132,  0.59197138,  0.98314453,  0.1142276,
  0.63429356,  0.01911331,  0.98560073,  0.42638865,  0.05303925,  0.2785799,
  0.66517311,  0.99737475,  0.56541296,  0.36455504,  0.52069008,  0.26070156,
  0.1162146,   0.02720099,  0.93103247,  0.47510255,  0.46227728,  0.77379236,
  0.3203669,   0.40769215,  0.00218079,  0.35174194,  0.93314201,  0.3495106 ]

class TestModelFactory(unittest.TestCase):
    def setUp(self):
        self.freq = "10Min"
        self.mf = ModelFactory(None, self.freq, "linear")

    def test_raises_on_invalid_appliance(self):
        self.assertRaises(UnsupportedAppliance, self.mf, invalid_appliance)

    def test_ok_on_valid_appliance(self):
        try:
            model = self.mf(valid_appliance)
        except UnsupportedAppliance:
            self.fail("getting a {} raised UnsupportedAppliance unexpectedly!".format(valid_appliance))
        self.assertIsInstance(model, ApplianceModel)
        self.assertEqual(model.name, valid_appliance)
        self.assertEqual(model.freq, self.freq)

    def test_can_generate_all_appliances(self):
        for appliance_key in self.mf.appliance_keys():
            try:
                model = self.mf(appliance_key)
            except UnsupportedAppliance:
                self.fail("getting a {} raised UnsupportedAppliance unexpectedly!".format(appliance_key))
            self.assertIsInstance(model, ApplianceModel)
            self.assertEqual(model.name, appliance_key)
            self.assertEqual(model.freq, self.freq)

    def test_can_override_daily_consumption(self):
        model = self.mf(valid_appliance, daily_consumption=100)
        self.assertEqual(model.daily_total, 100)

class TestApplianceModel(unittest.TestCase):
    def setUp(self):
        self.factory = ModelFactory(None, "1Min", "linear")
        self.appliance = self.factory(valid_appliance)

    def test_midnight_events(self):
        """passing in zeros should produce events at midnight"""
        days = 30
        events = self.appliance.events(days, start=datetime.datetime(2001, 1, 1), random_data=[0]*days)
        self.assertTrue((events.hour == 0).all())
        self.assertTrue((events.day == range(1, days+1)).all())

    def test_midnight_events_in_simulation(self):
        """passing in zeros to a simulation with a 1-minute cycle should produce consumption only at midnight"""
        days = 365
        cycle_length = 1
        freq = "30Min"
        data = self.appliance.simulation(days, cycle_length, freq, start=datetime.datetime(2001, 1, 1), random_data=[0]*days)
        self.assertEqual(len(data), days * 48)    # length of full dataset is correct
        totals = data.groupby(data.index.time).mean()
        self.assertTrue((totals[1:] == 0).all())
        self.assertEqual(totals[0], self.appliance.daily_total)

    def test_midnight_events_with_alternative_profile(self):
        """passing in zeros should produce events at midnight, even with a different profile"""
        days = 30
        cooking = self.factory('Cooking')
        events = self.appliance.events(days, start=datetime.datetime(2001, 1, 1), random_data=[0]*days, profile=cooking.profile)
        self.assertEqual(len(events), days)    # length of full dataset is correct
        self.assertTrue((events.hour == 0).all())
        self.assertTrue((events.day == range(1, days+1)).all())


    def test_events(self):
        """passing in a specific set of random data should produce events as expected"""
        days = 30
        events = self.appliance.events(days, start=datetime.datetime(2001, 1, 1), random_data=seed)

        result = [630, 512, 1015, 930, 1400, 482, 977, 72, 1405, 760,
                  376, 627, 1012, 1433, 902, 702, 856, 612, 485, 132,
                  1309, 808, 795, 1132, 663, 742, 5, 691, 1312, 689]

        self.assertTrue((events.hour*60 + events.minute == result).all())

    def test_events_with_alternative_profile(self):
        """passing in a specific set of random data should produce events as expected, even with a different profile"""
        days = 30
        cooking = self.factory('Cooking')
        events = self.appliance.events(days, start=datetime.datetime(2001, 1, 1), random_data=seed, profile=cooking.profile)
        result = [669, 493, 1038, 996, 1346, 461, 1020, 241, 1355, 826,
                  381, 665, 1037, 1416, 979, 753, 945, 644, 463, 304,
                  1238, 895, 878, 1098, 709, 802, 24, 740, 1241, 738]

        self.assertTrue((events.hour*60 + events.minute == result).all())

    def test_total_consumption(self):
        """
        test that the square-wave produced in simulation has correct properties
        passing in 0.5 to a simulation should produce a predictable square-wave
        with no overlap at midnight

        """
        days = 32
        cycle_length = 12
        freq = "1Min"
        data = self.appliance.simulation(days, cycle_length, freq, start=datetime.datetime(2001, 1, 1), random_data=[0.5]*days)
        self.assertEqual(len(data), days * 24 * 60)                 # length of full dataset is correct
        self.assertEqual(len(data[data > 0]), days * cycle_length)  # cycles are correct length
        # each daily total is very close to the stated value
        totals = data.groupby(data.index.date).sum()
        self.assertTrue((abs(totals - self.appliance.daily_total) < 1e-10).all())


if __name__ == "__main__":
    unittest.main()
