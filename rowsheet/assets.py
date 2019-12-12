import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.template import loader
from rowsheet.APISpec import APISpec
from django.utils.safestring import mark_safe

DEV_MODE = True

api_spec = APISpec(os.path.join(settings.BASE_DIR, "api"))

def index(request, asset="js"):

    # Hot-reload if DEV_MODE == True
    if DEV_MODE == True:
        api_spec = APISpec(os.path.join(settings.BASE_DIR, "api"))

    template = loader.get_template("rowsheet/assets/" + asset)
    import datetime
    context = {
        "api_spec": api_spec.get_config(),
        "now": str(datetime.datetime.utcnow()),
    }
    response = HttpResponse(template.render(context, request))
    response["Content-Type"] = "application/javascript"
    return response

urlpatterns = [
    path("<asset>", index),
]
