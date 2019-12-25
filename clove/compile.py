"""
This module is the main user callable interface to the resume compiler
"""

import json
import argparse

import jinja2

import clove

# Global variables
default_template = "template/markdown_basic.md"
default_output = "../output/resume.md"
default_num_projects = 6

def main(application_loc, userdata_loc, 
         template_loc=default_template, 
         output_loc=default_output,
         num_projects=default_num_projects):
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
    """

    # Open the provided JSON file locations
    with open(application_loc, "r") as f:
        application = json.load(f)

    with open(userdata_loc, "r") as f:
        userdata = json.load(f)

    # Verify that the loaded files are correctly structured
    clove.validate.userdata(userdata)
    clove.validate.application(application, userdata)

    # Filter the project list and replace the full list in userdata
    filtered_projects = clove.filter.sum_l2(
        userdata, application, num_projects
    )
    userdata["filtered_projects"] = filtered_projects

    # Write the output to the template and then to the output directory
    with open(template_loc, "r") as f:
        template = jinja2.Template(f)
    template.render(userdata)
    with open(output_loc, "w") as f:
        f.write(template)
    
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
    args = parser.parse_args()

    main(args.application_data, args.user_data,
        args.template, args.output, args.projects)
    