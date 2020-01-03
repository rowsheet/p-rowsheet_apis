import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.template import loader
from rowsheet.APISpec import APISpec

DEV_MODE = True

api_spec = APISpec(os.path.join(settings.BASE_DIR, "api"))

config = {
    "sidebar_width": 300,
}

def render_api_spec(request, version=None):

    # Hot-reload if DEV_MODE == True
    if DEV_MODE == True:
        api_spec = APISpec(os.path.join(settings.BASE_DIR, "api"))

    if version is None:
        return JsonResponse({"error", "You must specify a url version in the path."}, 400)
    return JsonResponse(api_spec.get_config().get(version))

def index(request, version="v1"):

    print("FUCKING INDEX")
    print(settings)

    # Hot-reload if DEV_MODE == True
    if DEV_MODE == True:
        api_spec = APISpec(os.path.join(settings.BASE_DIR, "api"))

    template = loader.get_template("rowsheet/index.html")
    context = {
        "version": version,
        "api_spec": api_spec.get_config()[version],
        "config": config,
    }
    return HttpResponse(template.render(context, request))

urlpatterns = [
    path("", index),
    path("<version>", index),
    path("api_spec/<version>", render_api_spec),
    path("api_spec/", render_api_spec),
]
