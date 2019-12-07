from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin

from rowsheet.api import handle

admin.autodiscover()

def catch_all(request):
    return HttpResponseRedirect("/docs/v1")

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^docs/", include("rowsheet.urls")),
    path("<version>/<service>/<module>/<command>", handle),
    path("", catch_all),
]
