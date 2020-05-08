{% extends "section.md" %}

{% block body %}

<p style="text-align: justfy">
    {% for interest in items %}
        {{ interest }} &bull;
    {% endfor %}
</p>

{% endblock body %}
