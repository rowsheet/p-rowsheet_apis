import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.urls import path
from rowsheet.APISpec import APISpec

# Search for APISpec config files in BASE_DIR/api_spec/[version].yaml.
def api_spec(request, version=None):

    # Request path must specify a version.
    if version is None:
        return JsonResponse({
            "error": "You must specify an API version",
        }, status=400)
    api_spec_filepath = os.path.join(
        settings.BASE_DIR,
        "api_spec/" + version + ".yaml"
    )

    # Version must exist.
    if os.path.exists(api_spec_filepath) != True:
        return JsonResponse({
            "error": "That API version doesn't exist",
        }, status=400)

    # All clear; load API Spec.
    api_spec = APISpec()
    api_spec.parse_config_file(api_spec_filepath)
    return JsonResponse(api_spec.get_config())

def index(request):
    return HttpResponse("RowSheet APIs")

urlpatterns = [
    path("", index),
    path("api_spec/<version>", api_spec),
    path("api_spec/", api_spec),
]
