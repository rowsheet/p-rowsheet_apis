from django import template
from django.utils.safestring import mark_safe
from django.template import Context, Template
import yaml

register = template.Library()

@register.simple_tag
def js_params(params):
    try:
        return ", ".join([param_name for param_name, _ in params.items()] + 
            ["success", "error"])
    except Exception as ex:
        return ", ".join(["success", "error"])

@register.simple_tag
def js_doc(command, indent=0):
    tabs = "".join(["    " for i in range(indent)])
    line = "".join(["-" for i in range(80 - indent*4 - 2)])
    start = "/*" + line
    doc = tabs + " * " + yaml.dump(command, line_break=False).replace("\n","\n" +
            tabs + " * ").strip(" ")
    end = tabs + line + "*/"
    return mark_safe("%s\n%s\n%s" % (start, doc, end))

@register.simple_tag
def command_url(request, vkey, skey, mkey, ckey, command):
    try:
        query_string = ""
        params = command.get("params")
        if command["method"].lower() == "get" and params is not None:
            query_string = "?" + "&".join([
                (pkey + "=\" + " + pkey + " + \"")
                for pkey, _ in params.items()])
        return mark_safe("/".join([
            vkey, skey, mkey, ckey,
        ]) + query_string)
    except Exception as ex:
        return str(ex)

@register.simple_tag
def command_data(method, params, indent):
    tabs = "".join(["    " for i in range(indent)])
    try:
        if method.lower() == "post":
            if params is not None:
                start = "data: {\n"
                lines = "\n".join([tabs + "    \"%s\": %s," % (pkey, pkey) for pkey, _ in params.items()])
                end = "\n" + tabs + "},"
                return mark_safe(start + lines + end)
        return ""
    except Exception as ex:
        return ""
