"""
Main user callable interface to the resume compiler
"""

import json
import argparse

import jinja2

from . import validate
from . import filter

# Global variables
default_template = "template/markdown_basic.md"
default_output = "../output/resume.md"
default_num_projects = 6
default_filter_norm = "mult"
default_derate = 1.0

filter_map = {
    "l2": filter.l2,
    "mult": filter.mult
}

def main(application_loc, userdata_loc, 
         template_loc=default_template, 
         output_loc=default_output,
         num_projects=default_num_projects,
         filter_norm=default_filter_norm,
         derate=default_derate):
    """Main resume compiling function callable by the user

    Parameters
    ----------
    application_loc: str
        File path to the JSON file describing the application
    userdata_loc: str
        File path to the JSON file describing the applicant's experience
    template_loc: str
        File path to the resume template to fill out
    output_loc: str
        File path to the desired output location
    num_projects: int
        Number of projects to include in the resume
    filter_norm: str
        Name of the filter norm function to use
    derate: float
        Derate value to be used to promote a variety of skills
        demonstrated. 1.0 -> No variety, 0.1 -> extreem variety
    """

    # Open the provided JSON file locations
    with open(application_loc, "r") as f:
        application = json.load(f)

    with open(userdata_loc, "r") as f:
        userdata = json.load(f)

    # Verify that the loaded files are correctly structured
    validate.userdata(userdata)
    validate.application(application, userdata)

    # Filter the project list and replace the full list in userdata
    filtered_projects = filter.apply(
        userdata, application, filter_map[filter_norm], num_projects, derate
    )
    userdata["filtered_projects"] = filtered_projects
    # Change tag names to full names
    for project in filtered_projects:
        if project["organization"] is not None:
            project["organization"] = userdata["organizations"][project["organization"]]["name"]
        skill_list = []
        for skill in project["skills"]:
            skill_list.append(userdata["skills"][skill]["name"])
        project["skills"] = ", ".join(skill_list)

    # Sort the skills by need and include them in the userdata
    filtered_skills = sorted(application["skills"], 
        key=lambda x: x["need"], reverse=True
    )
    for skill in filtered_skills:
        skill["ability"] = userdata["skills"][skill["name"]]["ability"]
        skill["name"] = userdata["skills"][skill["name"]]["name"]
    userdata["filtered_skills"] = filtered_skills

    # Update the name of the organization in work history
    for item in userdata["work_history"]:
        item["organization"] = userdata["organizations"][item["organization"]]["name"]

    # Write the output to the template and then to the output directory
    with open(template_loc, "r") as f:
        template = jinja2.Template(f.read())
    resume_out = template.render(userdata)
    with open(output_loc, "w") as f:
        f.write(resume_out)
    
if __name__ == "__main__":
    
    # Command line user interface using argparse
    parser = argparse.ArgumentParser(
        description="""
            Compile a resume from the given user data, application info and
            a resume template
            """
    )
    parser.add_argument("application_data",
        help="Location of the application data JSON file"
    )
    parser.add_argument("user_data",
        help="Location of the user data JSON file"
    )
    parser.add_argument("-t", "--template", 
        help="Location of the resume template file",
        default=default_template
    )
    parser.add_argument("-o", "--output",
        help="Output location for the compiled resume",
        default=default_output
    )
    parser.add_argument("-p", "--projects",
        help="Number of projects to include in the resume",
        type=int,
        default=default_num_projects
    )
    parser.add_argument("-n", "--norm",
        help="Filter that will be applied to score projects",
        type=str,
        choices=filter_map.keys(),
        default=default_filter_norm 
    )
    parser.add_argument("-d", "--derate",
        help="""Derate in scoring used for skills that have already 
                been included. Must be between 1.0 (no derate) 
                and 0.1 (massive derate)""",
        type=float,
        default=default_derate
    )
    args = parser.parse_args()

    # Check for errors in the user input
    if args.derate > 1.0 or args.derate < 0.1:
        parser.error("Derate value must be between 0.1 and 1.0")

    main(args.application_data, args.user_data,
        args.template, args.output, args.projects, 
        args.norm, args.derate)
    