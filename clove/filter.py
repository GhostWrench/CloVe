"""
Routines for filtering projects based on relevance
"""

import os
import math

from .util import schema_dir

def sum_l2(projects, skills, limit):
    """Filter project using the sum of the L2 norm of ability, need and
    project prestige

    Parameters
    ----------
    projects: list
        List of projects from the the user's userdata JSON file
    skills: list
        List of skills from an application JSON file
    limit: integer
        Number of projects to return

    Returns
    -------
    list
        List of projects ordered from most relevant to least
    """

    # Make a dictionary of application skills with their need level
    application_skills = {}
    for skill in skills:
        application_skills[skill["name"]] = skill["need"]

    # Create a list of project scores
    scores = []

    for project in projects:
        total_score = 0
        for skill in project["skills"]:
            if skill["name"] in application_skills:
                term1 = project["prestige"]
                term2 = skill["ability"]
                term3 = application_skills[skill["name"]]
                total_score += math.sqrt(term1**2 + term2**2 + term3**2)
        scores.append(total_score)

    # Sort the projects and return the tops ones
    sorted_indices = [i[0] for i in sorted(enumerate(scores), key=lambda x:x[1])]
    sorted_projects = [projects[i] for i in sorted_indices]
    max_index = max((len(projects), limit)) - 1
    return sorted_projects[0:max_index]

    
    
