import unittest

from cegads import (
    Scenario,
    ScenarioFactory,
    InvalidDataFileError,
    InvalidYearError,
    CEGADSException
)

invalid_year = "apple"
missing_year = 1100
valid_year = 2013
invalid_path = "invalid/path"

class TestScenarioFactory(unittest.TestCase):

    def test_raises_on_invalid_year(self):
        sf = ScenarioFactory()
        self.assertRaises(InvalidYearError, sf, invalid_year)

    def test_raises_on_missing_year(self):
        sf = ScenarioFactory()
        self.assertRaises(InvalidYearError, sf, missing_year)

    def test_ok_given_valid_year(self):
        sf = ScenarioFactory()
        try:
            sc = sf(valid_year)
        except CEGADSException as e:
            self.fail("getting scenario '{}' raised {} unexpectedly!".format(valid_year, e.__class__.__name__))
        self.assertIsInstance(sc, Scenario)


if __name__ == "__main__":
    unittest.main()
