"""Validation routines for various user data"""

import os
import json
import jsonschema

class LinkError(Exception):
    """Raised when there is a key value error in certain linked fields"""

    def __init__(self, key, object_name):
        message = "No valid link for '{0:s}' in '{1:s}'".format(
            key, object_name
        )
        super(LinkError, self).__init__(message)

def schema_dir():
    schema_dir = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "../schema"
    ))
    return schema_dir

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

    schema_loc = os.path.join(schema_dir(), "userdata.json")
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

def application(application_loc, userdata_loc):
    """Validate that an application JSON file is in the correct format

    This function will compare the application vs the schema as well as
    checking to make sure that the skills listed in the application are
    availble in the userdata. Throws errors if there are any and will 
    silently return nothing if there aren't.

    Parameters
    ----------
    application_loc: str
        Location of the application JSON file describing the job posting
    userdata_loc: str
        Location of the userdata JSON file describing the candidate
    """
    
    # Open the userdata, application and userdata schema
    schema_loc = os.path.join(schema_dir(), "application.json")
    with open(schema_loc, "r") as f:
        schema = json.load(f)
    
    with open(application_loc, "r") as f:
        application = json.load(f)

    with open(userdata_loc, "r") as f:
        userdata = json.load(f)

    # Create a list of validation errors
    validation_errors = []

    # Validate the application verus the schema
    try:
        jsonschema.validate(application, schema)
    except jsonschema.ValidationError as err:
        validation_errors.append(err)

    # Loop through each skill and make sure that it is present in userdata
    valid_skills = userdata["skills"].keys()
    for skill in application["skills"]:
        if not (skill["name"] in valid_skills):
            err = LinkError(skill["name"], "user data")
            validation_errors.append(err)
    
    # Raise errors if there are any
    if len(validation_errors):
        raise Exception(validation_errors)
    