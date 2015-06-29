"""test the modelData class"""
import unittest
from cegads.model_data import ModelData, InvalidDataFileError

cols = ['Cold Appliances', 'Cooking', 'Lighting', 'Audiovisual', 'ICT', 'wet_appliances', 'Water heating', 'Heating', 'Other', 'Unknown', 'Showers']

totals = {
    'Cold Appliances': 1553.8,
    'Cooking': 1206.5,
    'Water heating': 228.6,
    'Unknown': 2256.7,
    'Showers': 302.9,
    'ICT': 565.8,
    'Other': 474.2,
    'Heating': 569.7,
    'Lighting': 1273.1,
    'wet_appliances': 1171.8,
    'Audiovisual': 1469.8
}

class TestModelData(unittest.TestCase):
    def test_instantiates_with_none_path(self):
        """make sure passing None as the path generates a nice dataset"""
        md = ModelData(None)
        self.assertTrue((md._data.columns == cols).all())

    def test_fails_with_invalid_path(self):
        """make sure passing an invalid path raises a sane error"""
        self.assertRaises(InvalidDataFileError, ModelData, 'invalid/path')

class TestDefaultFileData(unittest.TestCase):
    def setUp(self):
        self.md = ModelData()

    def test_totals(self):
        "make sure the totals are all as expected"
        for key in cols:
            self.assertTrue(abs(self.md.total(key) - totals[key]) < 1e-10)

    def test_profile_length(self):
        "check the profiles are the right length at least"
        freqs = []
        for freq, l in [('10Min', 6*24), ('30Min', 48), ('2H', 12), ('12H', 2)]:
            p = self.md.profile('wet_appliances', freq, 'linear')
            self.assertEqual(len(p), l)

if __name__ == "__main__":
    unittest.main()
