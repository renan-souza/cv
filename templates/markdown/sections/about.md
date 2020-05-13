{% extends "section.md" %}

{% block body %}

<p style="text-align: justify;">
    {{ items }}
</p>


See 
<a href="data/{{personal.name.first}}-{{personal.name.last}}-CV-{{today}}.pdf" target='_blank' class="fa fa-download">
    Full CV
</a>
for complete information about education, professional experience, and technical skills.




{% endblock body %}
