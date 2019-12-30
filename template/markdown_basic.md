{{personal_info.name}}
===============================================================================
{% if personal_info.headline is not none -%}
{{personal_info.headline}}
-------------------------------------------------------------------------------
{% endif %}

{%- for key, value in personal_info.contact.items() %}
{{'%-20s' % key}}: {{value}}
{% endfor %}

CERTIFICATIONS
-------------------------------------------------------------------------------
{%- for item in certifications %}
### {{item.name}} @ {{item.organization}}
#### Date: {{item.date}}
{%- if item.description is string %}
{{item.description | wordwrap(78)}}
{% endif %}
{% endfor %}

SKILLS
-------------------------------------------------------------------------------

| Skill                                    | Ability (of 10) |
| ---------------------------------------- | --------------- |
{% for item in filtered_skills -%}
| {{ '%-40s' % item.name}} | {{ '%-15s' % item.ability}} |
{% endfor %}

PROJECTS
-------------------------------------------------------------------------------
{% for item in filtered_projects %}
### {{item.headline}}
#### {% if item.organization %}@ {{item.organization}}{% endif %}
#### Relevant Skills: {{item.skills}}
{%- if item.description is string %}
{{item.description | wordwrap(78)}}
{% endif %}
{% endfor %}

WORK HISTORY
-------------------------------------------------------------------------------
{% for item in work_history %}
### {{item.title}} @ {{item.organization}}
#### {{item.start_date}} to {{item.end_date if item.end_date else 'Present'}}
{%- if item.responsibilities is string %}
{{item.responsibilities | wordwrap(78) }}
{% endif %}
{% endfor %}
