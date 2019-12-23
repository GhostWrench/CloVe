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
        clove.validate.userdata(self.userdata)

    def test_application(self):
        clove.validate.application(
            self.application,
            self.userdata
        )

if __name__ == "__main__":
    unittest.main()
