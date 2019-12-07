from django import template
from django.utils.safestring import mark_safe

import json

register = template.Library()

@register.simple_tag
def pretty_json(content):
    out = """<pre>%s</pre>""" % json.dumps(
        content, indent=4, sort_keys=True) \
        .replace("\n","<br>").replace(" ", "&nbsp")
    return mark_safe(out)

@register.simple_tag
def replace(content, old, new):
    return content.replace(old, new)
