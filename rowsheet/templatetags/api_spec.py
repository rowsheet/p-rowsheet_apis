from django import template
from django.utils.safestring import mark_safe
from django.template import Context, Template

from .settings import COLORS

register = template.Library()

@register.simple_tag
def api_spec_label(spec):
    return ".".join([val for _, val in spec["route"].items()]) 

def highlight(content, color):
    return """
    <span style="color: %s">%</span>
    """ % (content, color)

def translate_data_type(spec_type):
    if spec_type == "int":
        return "integer"
    if spec_type == "bool":
        return "boolean"
    if spec_type == "str":
        return "string"
    return spec_type

@register.simple_tag
def endpoint_url(version, service, module, command, method):
    url_path = "/" + "/".join([version, service, module, command])
    method = """<div class='endpoint_http_method endpoind_http_method_%s'>%s</div>""" % (
        method,
        method,
    )
    return mark_safe(method + url_path)

@register.simple_tag
def api_spec_curl(request, version, skey, mkey, ckey, method, params=None):
    host = request.META['HTTP_HOST']
    url_path = "/".join([version, skey, mkey, ckey])
    curl_params = ""
    if params is None:
        curl_params = ""
    elif len(params) > 0:
        curl_params = "\n".join([
            """    <nobr>-d %s="<span class="pre_data_type">%s</span>" \\</nobr>""" % (
                pkey,
                translate_data_type(pkey)
            )
            for pkey, param in params.items()])
    color = "#f6968f"
    bearer_token = "BEARER_TOKEN"
    if request.user.is_authenticated:
        bearer_token = request.session.session_key
        color = COLORS["blue"]
    pre = """<pre>%s</pre>""" % (
        """
<nobr>curl -s %(host)s/%(url_path)s \</nobr>
    <nobr>
        -X <span class="pre_http_method pre_http_metho_%(method)s">
            %(method)s</span>
    \</nobr>
    <nobr>
    -u [<span style="color: %(color)s; font-weight: bold">%(bearer_token)s</span>]:
    %(uslash)s</nobr>
%(curl_params)s""" % {
            "host": host,
            "url_path": url_path,
            "method": method,

            "bearer_token": bearer_token,
            "color": color,
            "curl_params": curl_params,
            "uslash": "" if curl_params == "" else "\\"
        }
    ).strip("\\")
    return mark_safe(pre)

@register.simple_tag
def api_spec_guid(service, module, command):
    return "%s_%s_%s" % (service, module, command)

@register.simple_tag
def simple_function(spec):
    return spec["route"]["command"]
