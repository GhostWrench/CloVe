"""
This module is the main user callable interface to the resume compiler
"""

import json

import jinja2

import clove

def main(application_loc, userdata_loc):
    """Main resume compiling function callable by the user

    Parameters
    ----------
    application_loc: str
        File path to the JSON file describing the application
    userdata_loc: str
        File path to the JSON file describing the applicant's experience
    """

    # Open the provided JSON file locations
    with open(application_loc, "r") as f:
        application = json.load(f)

    with open(userdata_loc, "r") as f:
        userdata = json.load(f)

    # Verify that the loaded files are correctly structured
    clove.validate.userdata(userdata)
    clove.validate.application(application, userdata)

    
    