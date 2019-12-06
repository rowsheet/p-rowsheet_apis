import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import path
from rowsheet.APISpec import APISpec

# Search for APISpec config files in BASE_DIR/api_spec/[version].yaml.
def api_spec(request, version=None):
    api_spec = APISpec(os.path.join(settings.BASE_DIR, "api"))
    return JsonResponse(api_spec.get_config().get(version))

def index(request):
    return HttpResponse("RowSheet APIs")

urlpatterns = [
    path("", index),
    path("api_spec/<version>", api_spec),
    path("api_spec/", api_spec),
]
