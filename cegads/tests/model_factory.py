import unittest
import datetime

import numpy as np

from cegads.appliances.model import ModelFactory, UnsupportedAppliance, ApplianceModel

valid_appliance = 'Washing Machine'
invalid_appliance = 'invalid_appliance'

seed = [ 0.28190211,  0.14322136,  0.66798132,  0.59197138,  0.98314453,  0.1142276,
  0.63429356,  0.01911331,  0.98560073,  0.42638865,  0.05303925,  0.2785799,
  0.66517311,  0.99737475,  0.56541296,  0.36455504,  0.52069008,  0.26070156,
  0.1162146,   0.02720099,  0.93103247,  0.47510255,  0.46227728,  0.77379236,
  0.3203669,   0.40769215,  0.00218079,  0.35174194,  0.93314201,  0.3495106 ]

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

    def test_midnight_events_as_timeseries(self):
        """passing in zeros should produce events at midnight, in a rigid 10-minutely timeseries"""
        days = 365
        events = self.appliance.events_as_timeseries(days, start=datetime.datetime(2001, 1, 1), random_data=[0]*days)
        self.assertEqual(len(events), days * 24 * 6)    # length of full dataset is correct
        i = events[events==True].index                  # get the event datetimes
        self.assertEqual(len(i), days)                  # one event per day
        self.assertTrue((i.hour == 0).all())            # events are all at midnight
        self.assertTrue((i.minute == 0).all())          # events are all at midnight

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
        self.assertTrue((events.hour == 0).all())
        self.assertTrue((events.day == range(1, days+1)).all())


    def test_events(self):
        """passing in a specific set of random data should produce events as expected, even with a different profile"""
        days = 30
        events = self.appliance.events(days, start=datetime.datetime(2001, 1, 1), random_data=seed)
        result = [  630,  510, 1010,  930, 1400,
           480,  970,   60, 1400,  760,
           370,  630, 1010, 1430,  900,
           700,  850,  610,  480,  120,
          1310,  810,  790, 1130,  660,
           740,    0,  690, 1310,  690]
        self.assertTrue((events.hour*60 + events.minute == result).all())

    def test_events_with_alternative_profile(self):
        """passing in a specific set of random data should produce events as expected, even with a different profile"""
        days = 30
        cooking = self.factory('Cooking')
        events = self.appliance.events(days, start=datetime.datetime(2001, 1, 1), random_data=seed, profile=cooking.profile)
        result = [ 670,  490, 1040, 1000, 1340,
                   460, 1020,  240, 1350,  830,
                   380,  660, 1040, 1410,  980,
                   750,  940,  640,  460,  300,
                  1240,  890,  880, 1100,  710,
                   800,   20,  740, 1240,  740]
        self.assertTrue((events.hour*60 + events.minute == result).all())


if __name__ == "__main__":
    unittest.main()
