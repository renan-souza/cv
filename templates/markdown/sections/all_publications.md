# Publications and Patents

Please, feel free to reach me if you need a preprint of a paper not available here.

#### Contents

<ul>

{% for p in items %}

<li> <a href="#{{ p.title.lower().replace(" ","-")}}" > {{ p.title }} </a> </li>

{% endfor %}

</ul>



{% for p in items %}

## <a id="{{ p.title.lower().replace(" ","-")}}"><i class="fa fa-chevron-right"></i> {{ p.title }} </a> <a href="https://github.com/renan-souza/cv/blob/master/publications/{{ p.file }}" target="_blank"><i class="fa fa-code-fork" aria-hidden="true"></i></a>

<table class="table table-hover">
{{ p.details }}
</table>
{% endfor %}
