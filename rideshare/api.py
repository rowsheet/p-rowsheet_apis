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
from rideshare.models import DonationSubscription
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

@csrf_exempt
def passenger_cancel_ride_request(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    try:
        id = int(request.POST.get("id"))
        RideRequest.passenger_cancel_ride_request(app_user, id)
        return JsonResponse({
            "msg": "Passenger ride request canceled.",
        })
    except Exception as ex:
        print(str(ex))
        return JsonResponse({
            "location": "/set_location",
        }, status=500)

@csrf_exempt
def passenger_undo_cancel_ride_request(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    try:
        id = int(request.POST.get("id"))
        RideRequest.passenger_undo_cancel_ride_request(app_user, id)
        return JsonResponse({
            "msg": "Passenger ride request un-canceled.",
        })
    except Exception as ex:
        print(str(ex))
        return JsonResponse({
            "location": "/set_location",
        }, status=500)


@csrf_exempt
def driver_claim_pickup(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    try:
        id = int(request.POST.get("id"))
        RideRequest.driver_claim_pickup(app_user, id)
        return JsonResponse({
            "msg": "Claimed ride request for pickup."
        })
    except Exception as ex:
        print(str(ex))
        return JsonResponse({
            "location": "/set_location",
        }, status=500)


@csrf_exempt
def driver_cancel_pickup(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    try:
        id = int(request.POST.get("id"))
        RideRequest.driver_cancel_pickup(app_user, id)
        return JsonResponse({
            "msg": "Cancled pickup ride request."
        })
    except Exception as ex:
        print(str(ex))
        return JsonResponse({
            "location": "/set_location",
        }, status=500)


@csrf_exempt
def stripe_checkout_session_id(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    import stripe_util
    plan_id = request.POST.get("plan_id")
    if plan_id is None:
        raise Exception("Invalid plan_id: None.")
    session = stripe_util.create_checkout_session(plan_id)
    session_id = session["session_id"]
    amount = session["amount"]
    currency = session["currency"]
    product_id = session["product_id"]
    interval = session["interval"]

    DonationSubscription.objects.create(
        app_user=app_user,
        plan_id=plan_id,
        product_id=product_id,
        checkout_session_id=session_id,
        amount=amount,
        currency=currency,
        interval=interval,
        success=None,
    )

    return JsonResponse({
        "checkout_session_id": session_id,
    })


@csrf_exempt
def stripe_cancel_subscription_by_subscription_id(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    try:
        subscription_id = request.POST.get("subscription_id")
        if subscription_id is None:
            raise Exception("Missing subscription_id argument.")
        donation_subscription = DonationSubscription.objects.get(
            app_user=app_user,
            subscription_id=subscription_id,
        )
        if donation_subscription is None:
            raise Exception("Subscription doesn't exist this user.")
        import stripe_util
        # stripe_util.cancel_subscription_by_subscription_id(subscription_id)
        donation_subscription.deleted = True
        import pprint as pp
        print("------------------ DEBUG ")
        print(donation_subscription.subscription_id)
        print(donation_subscription.deleted)
        donation_subscription.save()
        return JsonResponse({}, status=200)
    except Exception as ex:
        print(str(ex))
        return JsonResponse({
            "error": "Unable to cancel subscription",
        }, status=500)
    return None

urlpatterns = [
    path("passenger_confirm_ride_request/", passenger_confirm_ride_request),
    path("passenger_cancel_ride_request/", passenger_cancel_ride_request),
    path("passenger_undo_cancel_ride_request/", passenger_undo_cancel_ride_request),
    path("driver_claim_pickup/", driver_claim_pickup),
    path("driver_cancel_pickup/", driver_cancel_pickup),
    path("stripe_checkout_session_id", stripe_checkout_session_id),
    path("strip_cancel_subscription_by_subscription_id", stripe_cancel_subscription_by_subscription_id),
]
