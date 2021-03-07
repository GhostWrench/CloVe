# CloVe
An optimizing CV/Resume compiler for nerds

## Introduction
CV + love == CloVe. CloVe is clever way to store all your skills,
certifications, project descriptions and work history all in a single 
(plain text) data file that can then be automatically filtered to fit a given 
job description and create a targeted resume.

## Compiling a CV / Resume
Compile an application with the following simple steps:

1. Create a user data JSON file that contains all the information about you 
   that an employer would be interested in. Use the example/userdata.json or 
   see the "Creating a User Data File" section for more information.

2. Create an application JSON file describing the skills that an employer
   is looking for in a job application. Use the example/application.json or
   see the "Creating an Application Data File" section for more information.

3. Using the user data and application data files call the compile script:
   ```
   $ python -m clove.compile ../application.json ../userdata.json
   ```
   For information on additional optional arguments use
   ```
   $ python -m clove.compile --help
   ```

## Creating a User Data File
Create a user data file that contains information about your skills, projects,
work history, certifications and organizations that you have worked with. The 
basic file structure is as follows:

```json
{
    "$schema": "schema/userdata.json",
    "personal_info": {
        "name": "..."
    },
    "skills": {},
    "organizations": {},
    "projects": [],
    "certifications": [],
    "work_history": []
}
```

### Skills
The "skills" object is where you list your skills and how good you are
at them (using the "ability" field). Like in the following example:

```json
    "skills": {
        "python": {
            "name": "Python",
            "ability": 10
        },
        "html": {
            "name": "HTML 5",
            "ability": 6
        }
    }
```
### Organizations
The organizations object is where you put all the organizations that you will
link to in your projects, work history and certification sections. 

```json
    "organizations": {
        "webschool": {
            "name": "Web Design School",
            "description": "A school where I learned to make websites",
            "location": "San Fransico, California"
        },
        "webcompany": {
            "name": "Web Design Company",
            "description": "A company that makes websites",
            "location": "San Fransisco, California"
        }
    }
```

### Projects
The "projects" list contains descriptions of all projects that you have 
worked on that you think is of interest to employers. Each project can be 
linked to multiple skills using the "skills" field. The "prestige" field 
can be used to ensure that projects you are more proud of are displayed 
more prominently on resumes that you compile. Construct this section 
according to the following example:

```json
    "projects": [
        {
            "headline": "Web Design Project",
            "description": "I made a website!",
            "prestige": 9,
            "skills": ["python", "html"],
            "organization": "webcompany"
        }
    ]
```

### Certifications
This list contains a list of certifications that you have obtained. Link them
to an organization using the organization field.

```json
    "certifications": [
        {
            "name": "Web Site Builder Cerfification",
            "organization": "webschool",
            "date": "2020-01-01"
        }
    ]
```

### Work History
Use the work_history list is where all of the positions that you have held go. 
Again, use the organization field to link it to the organization you were 
working for.

```json
    "work_history": [
        {
            "title": "Senior Website Engineer",
            "organization": "seagate",
            "start_date": "2020-02-01",
            "responsibilities": "I Build Websites"
        },
    ]

```

### Creating an Application Data File
An application file is what matches your skills and projects to a job
description. When you want to compile a resume to match a job you make a 
JSON file with the following structure:

```json
{
    "$schema": "schema/application.json",
    "title": "Website Developer",
    "skills": [
        {
            "name": "python",
            "need": 10
        },
        {
            "name": "html",
            "need": 10
        },
    ]
}
```

Use the "need" field to make sure that certain skills are displayed more
prominently on your resume.

## Running Tests

> python -m unittest