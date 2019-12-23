import unittest

import clove

class TestValidate(unittest.TestCase):

    def test_userdata(self):
        clove.validate.userdata("example/userdata.json")

    def test_application(self):
        clove.validate.application(
            "example/application.json",
            "example/userdata.json"
        )

if __name__ == "__main__":
    unittest.main()