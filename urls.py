from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^", include("rowsheet.urls")),
]
