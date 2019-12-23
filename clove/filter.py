"""
Routines for filtering projects based on relevance
"""

import os
import math

from .util import schema_dir

def sum_l2(userdata, application, limit):
    """Filter project using the sum of the L2 norm of ability, need and
    project prestige

    Parameters
    ----------
    userdata: dict
        Dictionary with the userdata JSON file describing the candidate
    application: dict
        Dictionary with the application JSON file describing the job posting
    limit: integer
        Number of projects to return

    Returns
    -------
    list
        List of projects ordered from most relevant to least
    """

    # Make a dictionary of application skills with their need level
    application_skills = {}
    for skill in application["skills"]:
        application_skills[skill["name"]] = skill["need"]

    # Create a list of project scores
    scores = []

    for project in userdata["projects"]:
        total_score = 0
        for skill in project["skills"]:
            if skill in application_skills:
                term1 = project["prestige"] # Prestige of the project
                term2 = userdata["skills"][skill]["ability"] # User's ability in the skill
                term3 = application_skills[skill] # Need for the skill in the application
                total_score += math.sqrt(term1**2 + term2**2 + term3**2)
        scores.append(total_score)

    # Sort the projects and return the tops ones
    sorted_indices = [i[0] for i in reversed(sorted(enumerate(scores), key=lambda x:x[1]))]
    sorted_projects = [userdata["projects"][i] for i in sorted_indices]
    min_index = min((len(userdata["projects"]), limit))
    return sorted_projects[0:min_index]
