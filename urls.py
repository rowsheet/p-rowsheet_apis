from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin

from rowsheet.api import handle

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^docs/", include("rowsheet.urls")),
    path("<version>/<service>/<module>/<method>", handle),
]
