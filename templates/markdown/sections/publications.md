# {{ name }}

Please, feel free to reach me if you need a preprint of a paper not available here.

#### Contents

<ul>

{% for p in items %}

<li> <a href="#--{{ p.title.lower().replace(" ","-")}}-" > {{ p.title }} </a> </li>

{% endfor %}

</ul>



{% for p in items %}

## <a id="{{ p.title.lower().replace(" ","-")}}"><a/> <i class="fa fa-chevron-right"></i> {{ p.title }} <a href="{{src.replace('github.com','raw.githubusercontent.com')}}/master/publications/{{ p.file }}"  target="_blank"><img src="/images/BibTeX.png" style="width:2.0em; border: 0" /></a>

<table class="table table-hover">
{{ p.details }}
</table>
{% endfor %}
