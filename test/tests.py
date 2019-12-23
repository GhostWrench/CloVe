import unittest
import json

import clove

class TestValidate(unittest.TestCase):

    def setUp(self):
        userdata_loc = "example/userdata.json"
        application_loc = "example/application.json"
        with open(userdata_loc, "r") as f:
            self.userdata = json.load(f)
        with open(application_loc, "r") as f:
            self.application = json.load(f)

    def test_userdata(self):
        """Test userdata validation with the example data"""
        clove.validate.userdata(self.userdata)

    def test_application(self):
        """Test application validation with the example data"""
        clove.validate.application(
            self.application,
            self.userdata
        )

    def test_filter_sum_l2(self):
        """Test the sum_l2 filter on example userdata"""
        filtered_projects = clove.filter.sum_l2(
            self.userdata, self.application, 6
        )
        self.assertEqual(len(filtered_projects), 6)

if __name__ == "__main__":
    unittest.main()
