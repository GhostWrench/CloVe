"""Validation routines for various user data"""

import os
import json
import jsonschema

class LinkError(Exception):
    """Raised when there is a key value error in certain linked fields"""

    def __init__(self, key, object_name):
        self.message = "No valid link for '{0:s}' in '{1:s}'".format(
            key, object_name
        )

def userdata(userdata_loc):
    """Validate the user data provided as JSON

    This function will compare against the schema and make sure that all linked
    fields are pointing to an appropriate field within the data. Throws an
    Exception if errors have occured, otherwise completes and doesn't return
    anything.

    Parameters
    ----------
    userdata_loc: str
        Location of the user data file to be validated
    """

    # Open the userdata file and schema as json
    with open(userdata_loc, 'r') as f:
        userdata = json.load(f)

    file_loc = os.path.dirname(__file__)
    relative_loc = "../schema/userdata.json"
    schema_loc = os.path.normpath(os.path.join(file_loc, relative_loc)) 
    with open(schema_loc, 'r') as f:
        schema = json.load(f)

    # Create a list of validation errors
    validation_errors = []

    # Validate the userdata vs the schema
    try:
        jsonschema.validate(userdata, schema)
    except jsonschema.ValidationError as err:
        validation_errors.append(err)
        
    # Check that the skills and organizations linked to a project are valid
    valid_skills = userdata["skills"].keys()
    valid_organizations = userdata["organizations"].keys()
    for project in userdata["projects"]:
        if not ("organization" in project.keys()):
            pass
        elif not (project["organization"] in valid_organizations):
            err = LinkError(project["organization"], project["headline"])
            validation_errors.append(err)

        for skill in project["skills"]:
            if not (skill in valid_skills):
                err = LinkError(skill, project["headline"])
                validation_errors.append(err)

    # Check that all the organizations linked to work_history are valid
    for job in userdata["work_history"]:
        if not (job["organization"] in valid_organizations):
            err = LinkError(job["organization"], job["title"])
            validation_errors.append(err)

    # Check that all organizations linked to certifications are valid
    for cert in userdata["certifications"]:
        if not (cert["organization"] in valid_organizations):
            err = LinkError(cert["organization"], cert["name"])
            validation_errors.append(err)

    # Raise errors if there are any
    if len(validation_errors):
        raise Exception(validation_errors)
