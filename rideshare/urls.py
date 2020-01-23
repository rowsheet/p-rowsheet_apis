import os
from django.urls import path
from rideshare import views

urlpatterns = [
    path("", views.index),
    path("phone_verification/", views.phone_verification),
    path("code_verification/", views.code_verification),
    path("main_screen/", views.main_screen),
    path("set_location/", views.set_location),
    path("account/", views.account),
    path("profile/", views.profile),
]
