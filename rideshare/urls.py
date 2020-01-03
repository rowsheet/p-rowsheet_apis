from django.urls import path
from rideshare import views

urlpatterns = [
    path("", views.index),
    path("main_screen", views.main_screen),
    path("verification_phone", views.verification_phone),
    path("verification_code", views.verification_code),
    path("set_location", views.set_location),
    path("set_location_later", views.set_location_later),
    path("create_account", views.create_account),
    path("account_created", views.account_created),
    path("account", views.account),
]
