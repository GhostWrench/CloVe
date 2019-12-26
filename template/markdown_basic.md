{{personal_info.name}}
===============================================================================
{% if personal_info.headline is not none -%}
{{personal_info.headline}}
-------------------------------------------------------------------------------
{% endif %}

{%- for key, value in personal_info.contact.items() -%}
{{key}}: {{value}}
{% endfor %}

CERTIFICATIONS
-------------------------------------------------------------------------------
{%- for item in certifications %}
{{item.name}} | {{item.organization}}
Date: {{item.date}}
{{item.description}}
{% endfor %}

SKILLS
-------------------------------------------------------------------------------
{% for item in skills.items() -%}
{{item[1].name}}, ability: {{item[1].ability}}
{% endfor %}

PROJECTS
-------------------------------------------------------------------------------
{% for item in filtered_projects %}
{{item.headline}}
{% if item.organization %}@ {{item.organization}}{% endif %}
Relevant Skills:{% for skill in item.skills %} {{skill}} {% endfor %}
{{item.description}}
{% endfor %}

WORK HISTORY
-------------------------------------------------------------------------------
{% for item in work_history %}
{{item.title}} | {{item.organization}}
{{item.start_date}} to {{item.end_date if item.end_date else 'Present'}}
{{item.responsibilities}}
{% endfor %}
