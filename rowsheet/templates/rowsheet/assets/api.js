/*------------------------------------------------------------------------------

THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT THIS FILE.

------------------------------------------------------------------------------*/
{% load assets %}{% load basic %}
var API_SERVER_URL = "{{ request.build_absolute_uri }}"

var api = {
{% for vkey, version in api_spec.items %}
/*------------------------------------------------------------------------------
 * VERSION: {{ vkey }}
------------------------------------------------------------------------------*/

{{ vkey }}: {
        {% for skey, service in version.services.items %}
        /*----------------------------------------------------------------------
         * SERVICE: {{ skey }}
        ----------------------------------------------------------------------*/

        {{ skey }}: {
            {% for mkey, module in service.modules.items %}
            /*------------------------------------------------------------------
             * MODULE: {{ mkey }}
            ------------------------------------------------------------------*/

            {{ mkey }}: {
                {% for ckey, command in module.commands.items %}
                {% js_doc command 4 %}
                {{ ckey }}: function({% js_params command.params %}) {
                    return Promise.resolve($.ajax({
                        method: "{{ command.method }}",
                        url: API_SERVER_URL + "/{% command_url request vkey skey mkey ckey command %}",
                        {% command_data command.method command.params 6 %}
                        headers: { "Authorization": "Bearer " + getCookie("session_id") },
                    }));
                },
                {% endfor %}
            },
            {% endfor %}
        },
        {% endfor %}
    },
{% endfor %}
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

console.log("api.js: {{now}}");
