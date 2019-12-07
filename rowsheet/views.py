from django.http import HttpResponse, JsonResponse
from django.template import loader

from .utils import rdump
from .view_data import load_api_spec

import os, json

def api_docs(request):
    text = "DATA: %s%s" % (
            request.META['HTTP_HOST'],
            request.META['PATH_INFO'],
        )
    return HttpResponse(text)

config = {
    "sidebar_width": 300,
}

def index(request):
    template = loader.get_template("rowsheet/index.html")
    api_spec, table_of_contents = load_api_spec()
    context = {
        "api_spec": api_spec,
        "table_of_contents": table_of_contents,
        "config": config,
    }
    return HttpResponse(template.render(context, request))
