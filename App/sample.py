 {% if row[0] == data.globalSession.pid %}
                  {% set bg_class = "bg-danger" %}
                {% else %}
                  {% set bg_class = "bg-success" %}
                {%endif%}
                <div class="small-box {{bg_class}}">