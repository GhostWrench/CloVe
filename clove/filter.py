"""
Routines for filtering projects based on relevance
"""

import os
import math

def l2(p, a, n):
    """L2 Norm of the provided values"""
    return math.sqrt(p**2 + a**2 + n**2)

def mult(p, a, n):
    """Multiplication of the provided values"""
    return p * a * n


def apply_without_skill_derate(userdata, application, normfunc, limit):
    """Filter project using a norm function that takes ability, need and
    project prestige as parameters

    NOTE: This function is mostly unused for anything other than testing
    due to the fact that it should be functionally exactly the same as
    apply when the derate is set to 1.0

    Parameters
    ----------
    userdata: dict
        Dictionary with the userdata JSON file describing the candidate
    application: dict
        Dictionary with the application JSON file describing the job posting
    normfunc: func
        Function that takes as input (project prestige, skill ability and skill need)
        and returns a score that will be summed for each skill in the project to
        obtain the overall score
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
                prestige_term = project["prestige"]
                ability_term = userdata["skills"][skill]["ability"]
                need_term = application_skills[skill]
                total_score += normfunc(prestige_term, ability_term, need_term)
        scores.append(total_score)

    # Sort the projects and return the tops ones
    sorted_indices = [i[0] for i in sorted(enumerate(scores), key=lambda x:x[1], reverse=True)]
    sorted_projects = [userdata["projects"][i] for i in sorted_indices]
    min_index = min((len(userdata["projects"]), limit))
    return sorted_projects[0:min_index]


def apply(userdata, application, normfunc, limit, derate_value=0.9):
    """Filter project using a norm function that takes ability, need and
    project prestige as parameters. Will also generate a term that decreases
    the value a skill adds for everytime it is included in the resume to
    promote a larger variety of projects

    Parameters
    ----------
    userdata: dict
        Dictionary with the userdata JSON file describing the candidate
    application: dict
        Dictionary with the application JSON file describing the job posting
    normfunc: func
        Function that takes as input (project prestige, skill ability and skill need)
        and returns a score that will be summed for each skill in the project to
        obtain the overall score
    limit: integer
        Number of projects to return
    derate_value: number
        Amount to derate for skills that have already been demonstrated by a
        project.

    Returns
    -------
    list
        List of projects ordered from most relevant to least
    """

    # Make a dictionary of application skills with their need level
    application_skills = {}
    skill_derate = {}
    for skill in application["skills"]:
        application_skills[skill["name"]] = skill["need"]
        skill_derate[skill["name"]] = 0

    # Create a list of projects that have already been demonstrated so they
    # are not repeated
    used_projects_idx = []
    return_projects = []

    for _ in range(0, limit):

        # Create a new array of scores to be filled out
        scores = list()

        # Rather inefficient brute force loop, but since the number of elements
        # is small, it should be OK
        for project in userdata["projects"]:
            total_score = 0
            total_derate = 0
            for skill in project["skills"]:
                if skill in application_skills:
                    total_derate += skill_derate[skill]
                    prestige_term = project["prestige"]
                    ability_term = userdata["skills"][skill]["ability"]
                    need_term = application_skills[skill]
                    total_score += (derate_value**total_derate) * normfunc(prestige_term, ability_term, need_term)
            scores.append(total_score)

        # Sort the projects and return the tops ones
        sorted_indices = [i[0] for i in sorted(enumerate(scores), key=lambda x:x[1], reverse=True)]
        # Search for the top project index that has not been used
        search_idx = 0
        append_idx = sorted_indices[search_idx]
        while (append_idx in used_projects_idx):
            search_idx += 1
            append_idx = sorted_indices[search_idx]
        return_projects.append(userdata["projects"][append_idx])
        # Note used skills and projects
        used_projects_idx.append(append_idx)
        used_skills = userdata["projects"][append_idx]["skills"]
        for uskill in used_skills:
            if uskill in skill_derate.keys():
                skill_derate[uskill] += 1
    
    return return_projects
