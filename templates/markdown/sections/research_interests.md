{% extends "section.md" %}

{% block body %}

<p style="text-align: justfy">
    {% for interest in items %}
        {{ interest }}{% if loop.index < loop.length %} &bull;{%  endif %} 
    {% endfor %}
</p>



{% endblock body %}
