from django.http import JsonResponse, HttpResponse
from django.urls import path

def api_spec(request):
    return JsonResponse({
        "data": "APISpec Hasn't been implemented yet.",
    })

def index(request):
    return HttpResponse("RowSheet APIs")

urlpatterns = [
    path("", index),
    path("api_spec/", api_spec),
]
