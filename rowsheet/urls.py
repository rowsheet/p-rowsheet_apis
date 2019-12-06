from django.http import HttpResponse
from django.urls import path

def index(request):
    return HttpResponse("RowSheet APIs")

urlpatterns = [
    path("", index),
]
