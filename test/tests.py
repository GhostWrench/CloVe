import unittest
import json

import clove

class DoTests(unittest.TestCase):

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

    def test_filter_l2(self):
        """Test the sum_l2 filter on example userdata"""
        filtered_projects = clove.filter.apply_without_skill_derate(
            self.userdata, self.application, clove.filter.l2, 6
        )
        self.assertEqual(len(filtered_projects), 6)

    def test_filter_derate(self):
        """Test that the skill derate filter with no derate value
        returns the same things as the non-derated filter
        """
        filtered_projects = clove.filter.apply_without_skill_derate(
            self.userdata, self.application, clove.filter.l2, 6
        )
        filtered_project_derate = clove.filter.apply(
            self.userdata, self.application, clove.filter.l2, 6, 1.0
        )
        self.assertListEqual(
            filtered_projects, filtered_project_derate
        )

    def test_filter_derate2(self):
        """Test that the skill derate filter with a large derate
        does not return the same things as the non-derated filter
        """
        filtered_projects = clove.filter.apply_without_skill_derate(
            self.userdata, self.application, clove.filter.mult, 6
        )
        filtered_project_derate = clove.filter.apply(
            self.userdata, self.application, clove.filter.mult, 6, 0.8
        )
        with self.assertRaises(Exception):
            self.assertListEqual(
                filtered_projects, filtered_project_derate
            )

if __name__ == "__main__":
    unittest.main()
