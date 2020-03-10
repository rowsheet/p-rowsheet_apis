from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import redirect
# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import path, include

from rideshare.models import AppUser
from rideshare.models import Pronoun
from rideshare.models import Accommodation
from rideshare.models import RideRequest
from rideshare.models import OldRideRequest
from rideshare.models import OldDriverSignup

import rowsheet.utils as rs_utils
import requests
import json

import googlemaps
from datetime import datetime
import time

def load_app_user(request):
    if not request.user.is_authenticated:
        return None, redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user)
    if app_user.phone_number is None:
        print("NEED PHONE NUMBER")
        return None, redirect("/phone_verification")
    if not app_user.phone_verified:
        print("NEED PHONE VERIFICATION")
        return None, redirect("/code_verification")
    return app_user, None

@csrf_exempt
def passenger_confirm_ride_request(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    try:
        ride_request = RideRequest.objects.get(
            app_user=app_user,
            in_setup=True,
        )
        ride_request.status = "REQ_2"
        ride_request.in_setup = None
        ride_request.save()
        return JsonResponse({
            "msg": "Successfully confirmed this ride request.",
        })
    except Exception as ex:
        print(str(ex))
        return JsonResponse({
            "location": "/set_location",
        }, status=302)


urlpatterns = [
    path("passenger_confirm_ride_request/", passenger_confirm_ride_request),
]
