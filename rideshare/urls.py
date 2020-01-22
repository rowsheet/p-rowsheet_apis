import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.template import loader

def index(request, version="v1"):

    template = loader.get_template("rideshare/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

urlpatterns = [
    path("", index),
]
