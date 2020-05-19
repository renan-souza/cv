# Talks, Presentations, and Events Participation


Please, feel free to reach me if you need a presentation not available here.

<br/>
<br/>

<table class="table table-hover">
{% for event in items %}
<tr>  

  <td><b>{{ event.name }}</b> 
    {% if event.page %}
        <a href="{{event.page}}" target="_blank"><img src="/images/external-link.png" style="width: 1.2em; border: 0" /></a>
    {% endif %} in 
    {{event.place}}
    <br/>
    {% if event.subevents %}
        {% for subevent in event.subevents %} 
            <i>{{ subevent.name }}</i>
            {% if subevent.page %}
                <a href="{{subevent.page}}" target="_blank"><img src="/images/external-link.png" style="width: 1.2em; border: 0" /></a>
            {% endif %}
            <br/>
            {% if subevent.talks %}
                <ul>
                {% for talk in subevent.talks %}
                    <li>
                     {{ talk.title }},
                       {{ talk.kind }}
                       {% if talk.link %}
                           <a href="{{ talk.link }}" target="_blank">online</a>                                
                       {% endif %}
                    </li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endfor %}
    {% elif event.talks %}
        <ul>
            {% for talk in event.talks %}
               <li>
                 {{ talk.title }},
                   {{ talk.kind }}
                   {% if talk.link %}
                       , <a href="{{ talk.link }}" target="_blank">link</a>                                
                   {% endif %}
               </li> 
            {% endfor %}            
        </ul>
        
    {% endif %}
    
    
  
  
  </td>
  <td class='col-md-0'  style="text-align: center; vertical-align: middle;">{{ event.year }} </td>
  

  
  
</tr>
{% endfor %}
</table>



