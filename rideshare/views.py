from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import redirect
# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rideshare.models import AppUser
from rideshare.models import Pronoun
from rideshare.models import Accommodation
from rideshare.models import RideRequest
from rideshare.models import RideDonation
from rideshare.models import DonationSubscription
from rideshare.models import OldRideRequest
from rideshare.models import OldDriverSignup

import rowsheet.utils as rs_utils
import requests
import json

import googlemaps
from datetime import datetime
import time

from twilio.rest import Client


def send_text_message(body):
    account_sid = "AC24fc9ac27dee145f04d855b99b666ab8"
    auth_token = "08da7fc65a1b8163f17aa324ddef479d"
    client = Client(account_sid, auth_token)
    if settings.DEPLOYMENT_MODE != "DEVELOPMENT":
        num=['+14155745023','+15404540846', '+14158672671', '+16464138190', '+17203643760']
    else:
        num = ['+15404540846', '+17203643760'];  # DEV ONLY
    for i in range(0, len(num)):
        message = client.messages.create(
            num[i],
            from_="+14159939395",
            body=body)


def send_confirmation_text_message(body, to):
    account_sid = "AC24fc9ac27dee145f04d855b99b666ab8"
    auth_token = "08da7fc65a1b8163f17aa324ddef479d"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=to,
        from_="+14159939395",
        body=body)


# def send_phone_verification_text(body, to):
#     account_sid = "AC24fc9ac27dee145f04d855b99b666ab8"
#     auth_token  = "08da7fc65a1b8163f17aa324ddef479d"
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         to=to,
#         from_="+14159939395",
#         body=body)

"""-----------------------------------------------------------------------------
"SITE" (Old Site Pages)
-----------------------------------------------------------------------------"""


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def send_email(email_to, body, api_key):
    r = requests.post(
        "https://emailer.rowsheet.com/",
        data=json.dumps({
            "api_key": api_key,
            "to": email_to,
            "subject": "Ride Request",
            "body": body,
        }),
        headers={'content-type': 'application/json'}
    )
    return r


def validate_ajax_post(request):
    command = request.POST.get("command")
    if command is None:
        raise Exception("Command is none")
    recaptcha_token = request.POST.get("_grecaptcha_token")
    if recaptcha_token is None:
        raise Exception("Missing reCaptcha token")
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": "6LeoZbYUAAAAAJAN7NGGbFuT8qNKGPdKyqG6IgRR",
            "response": recaptcha_token,
            "remoteip": request.META.get('REMOTE_ADDR'),
        }
    )
    if response.status_code != 200:
        raise Exception("Non-200 reCaptcha response.")
    response_obj = json.loads(response.text, encoding="utf-8")

    success = response_obj.get("success")
    if success is None:
        raise Exception("Unparsable reCaptcha response (no 'success').")
    if not success:
        raise Exception("False reCaptcha success.")

    score = response_obj.get("score")
    if score is None:
        raise Exception("Unparsable reCaptcha response (no 'score').")
    if score < 0.7:
        raise Exception("Insufficient reCaptcha score.")

    data = dict(request.POST)
    data.pop("command")
    data.pop("_grecaptcha_token")

    return command, request.POST


"""-----------------------------------------------------------------------------
DEMO
-----------------------------------------------------------------------------"""


def demo_google_maps(request):
    return render(request, "rideshare/demo/google_maps.html")


"""-----------------------------------------------------------------------------
PAGES
-----------------------------------------------------------------------------"""


@csrf_exempt
def index(request):
    if request.method == "POST":

        try:
            command, data = validate_ajax_post(request)
        except Exception as ex:
            print("ERROR: " + str(ex))
            return HttpResponse("Invalid request", 400)

        import pprint as pp
        pp.pprint(data)

        if command == "request_a_ride":
            try:
                send_text_message("""
New request!

Date: %s
Time (0-23hrs): %s
Pick up: %s
Drop off: %s
Phone: %s
""" % (
                    str(data.get("pickup_date")),
                    str(data.get("pickup_time")),
                    str(data.get("start_location")),
                    str(data.get("end_location")),
                    str(data.get("phone_number")),
                ))
            except Exception as ex:
                print(str(ex))

            try:
                send_confirmation_text_message(
                    "We have received your request for a ride to %s from %s on %s at %s. Please contact us at 14155745023 for assistance." % (
                        str(data.get("end_location")),
                        str(data.get("start_location")),
                        str(data.get("pickup_date")),
                        str(data.get("pickup_time")),
                    )
                    ,
                    ("+1" + str(data.get("phone_number")
                                )))
            except Exception as ex:
                print(str(ex))

            OldRideRequest.objects.create(
                name=data.get("name"),
                end_location=data.get("end_location"),
                start_location=data.get("start_location"),
                phone_number=data.get("phone_number"),
                pickup_time=data.get("pickup_time"),
                pickup_date=data.get("pickup_date"),
                pronoun=data.get("pronoun"),
                special_req=data.get("special_req"),
                num_bags=data.get("num_bags"),
                passenger_count=data.get("passenger_count"),
            )
            return HttpResponse("Request Received! Please check your phone for an SMS confirmation.", status=200)
        if command == "driver_signup":
            OldDriverSignup.objects.create(
                comments=data.get("comments"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                pronoun=data.get("pronoun"),
                contact_email=data.get("contact_email"),
                contact_phone=data.get("contact_phone"),
                smartphone_type=data.get("smartphone_type"),
                vehicle_doors=data.get("vehicle_doors"),
                vehicle_make=data.get("vehicle_make"),
                vehicle_model=data.get("vehicle_model"),
                vehicle_year=data.get("vehicle_year"),
                yes_no_criminal_history=str2bool(data.get("yes_no_criminal_history")),
                yes_no_insurance=str2bool(data.get("yes_no_insurance")),
                yes_no_square=str2bool(data.get("yes_no_square")),
            )
            return HttpResponse("Submitted!", status=200)

        return JsonResponse({
            "data": "OK"
        }, status=200)

    return render(request, "rideshare/site/index.html")


def for_drivers(request):
    return render(request, "rideshare/site/for-drivers.html")


def for_riders(request):
    return render(request, "rideshare/site/for-riders.html")


def why_homobiles(request):
    return render(request, "rideshare/site/why-homobiles.html")


def signup(request):
    return render(request, "rideshare/site/signup.html")


def press(request):
    return render(request, "rideshare/site/press.html")


"""-----------------------------------------------------------------------------
Common Helper Functions
-----------------------------------------------------------------------------"""


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
def geocode(request):
    try:
        if not request.POST:
            return JsonResponse({
                "error": "No data"
            }, status=400)
        else:
            start_address = request.POST.get("start_address")
            end_address = request.POST.get("end_address")
            print("DEBUG")
            print(start_address)
            print(end_address)
            if start_address is None:
                return JsonResponse({
                    "error": "Start address is required.",
                }, status=400)
            if start_address == "":
                return JsonResponse({
                    "error": "Start address is required.",
                }, status=400)
            if end_address is None:
                return JsonResponse({
                    "error": "Destination address is required."
                }, status=400)
            if end_address == "":
                return JsonResponse({
                    "error": "Destination address is required."
                }, status=400)
            gclient = googlemaps.Client(
                key=settings.GOOGLE_MAPS_API_KEY)
            # Get start_address info
            start_results = gclient.geocode(start_address)
            start_place_id = start_results[0]["place_id"]
            start_lat = start_results[0]["geometry"]["location"]["lat"]
            start_lng = start_results[0]["geometry"]["location"]["lng"]
            # Get end_address info
            end_results = gclient.geocode(end_address)
            end_place_id = end_results[0]["place_id"]
            end_lat = end_results[0]["geometry"]["location"]["lat"]
            end_lng = end_results[0]["geometry"]["location"]["lng"]
            return JsonResponse({
                "start_place_id": start_place_id,
                "start_lat": start_lat,
                "start_lng": start_lng,
                "end_place_id": end_place_id,
                "end_lat": end_lat,
                "end_lng": end_lng,
            }, status=200)
    except Exception as ex:
        print(str(ex))
        return JsonResponse({
            "error": "Unknown error occurred",
        }, status=500)


"""-----------------------------------------------------------------------------
PAGES (Public and On-boarding)
-----------------------------------------------------------------------------"""


def get_started(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user)
    context = {
        # Sidebar info.
        "app_user": app_user,
        # Page info.
    }
    return render(request, "rideshare/pages/get_started.html", context)


def phone_verification(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user)

    if app_user.phone_verified == True:
        return redirect("/phone_number")

    error = ""

    if request.method == "POST":
        if not request.POST:
            error = "Invalid request."
        else:
            phone_number = request.POST.get("phone_number")
            if phone_number is None or phone_number == "":
                error += "Phone number required. "

        if error == "":
            app_user = AppUser.objects.get(
                django_account=request.user)
            app_user.phone_number = phone_number
            app_user.save()
            return redirect("/code_verification")

    context = {
        # Form info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        # Page info.
        "user_id": request.user.id,
        "app_user": app_user,
        "phone_number": app_user.phone_number,
        "phone_verified": app_user.phone_verified,
    }
    return render(request, "rideshare/pages/phone_verification.html", context)


def code_verification(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user)

    if app_user.phone_number is None:
        return redirect("/phone_verification")
    if app_user.phone_verified == True:
        return redirect("/phone_number")

    error = ""

    if request.method == "POST":
        if not request.POST:
            error = "Invalid request."
        else:
            verification_code = request.POST.get("verification_code")
            if verification_code is None or verification_code == "":
                error += "Verification code required. "

        if error == "":
            app_user = AppUser.objects.get(
                django_account=request.user)
            if verification_code == app_user.phone_verification_code:
                app_user.phone_verified = True
                app_user.save()
                return redirect("/main_screen")
            else:
                error = "Invalid code."

    context = {
        # Form info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        # Page info.
    }
    return render(request, "rideshare/pages/code_verification.html", context)


"""-----------------------------------------------------------------------------
PAGES (Authenticated)
-----------------------------------------------------------------------------"""


def main_screen(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    in_setup = False
    start_address = None
    start_place_id = None
    end_address = None
    end_place_id = None
    pickup_time = None
    pickup_date = None

    try:
        ride_request = RideRequest.objects.get(
            app_user=app_user,
            in_setup=True,
        )
    except Exception as ex:
        ride_request = None

    if ride_request is not None:
        in_setup = True
        start_address = ride_request.start_address
        start_place_id = ride_request.start_place_id
        end_address = ride_request.end_address
        end_place_id = ride_request.end_place_id

    sidebar_info = RideRequest.rider_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        "sidebar_info": sidebar_info,
        # Page info.
        "in_setup": in_setup,
        "start_address": start_address,
        "end_address": end_address,
        "originPlaceId": start_place_id,
        "destinationPlaceId": end_place_id,
    }
    return render(request, "rideshare/pages/main_screen.html", context)


@csrf_exempt
def set_location(request):
    # Check basic user info (logged in and valid phone)
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    # Set default ride request vars for the view. Get this
    # data from the RideRequest object associated with the
    # app_user. This data will be used to populate the template
    # context form values.
    start_address = ""
    start_place_id = ""
    start_lat = ""
    start_lng = ""
    end_address = ""
    end_place_id = ""
    end_lat = ""
    end_lng = ""
    pickup_timestamp = ""

    try:
        ride_request = RideRequest.objects.get(
            app_user=app_user,
            in_setup=True,
        )
        if ride_request is not None:
            print("RIDE REQUEST RECEIVED")
        else:
            print("NO RIDE REQUEST")
    except Exception as ex:
        ride_request = None

    error = ""

    print("GOT REQUEST")
    if request.method == "POST":
        print("GOT POST")
        if not request.POST:
            error = "Invalid request."
            return JsonResponse({
                start_address: "start_address",
                start_place_id: "start_place_id",
                end_address: "end_address",
                end_place_id: "end_place_id",
            }, status=200)
        else:
            start_address = request.POST.get("start_address")
            start_place_id = request.POST.get("start_place_id")
            start_lat = request.POST.get("start_lat")
            start_lng = request.POST.get("start_lng")
            end_address = request.POST.get("end_address")
            end_place_id = request.POST.get("end_place_id")
            end_lat = request.POST.get("end_lat")
            end_lng = request.POST.get("end_lng")
            # We need the "pickup_timestamp", but from the form, we
            # can only have the pickup_date and pickup_time, so we
            # have to extrapolate from that.
            pickup_time = request.POST.get("pickup_time")
            pickup_date = request.POST.get("pickup_date")
            timezone_offset = request.POST.get("timezone_offset")
            if start_address == "":
                error = "Invalid start address."
            if start_place_id == "":
                error = "Invalid start address."
            if start_lat == "":
                error = "Invalid start address."
            if start_lng == "":
                error = "Invalid start address."
            if end_address == "":
                error = "Invalid end address."
            if end_place_id == "":
                error = "Invalid end address."
            if end_lat == "":
                error = "Invalid end address."
            if end_lng == "":
                error = "Invalid end address."
            if pickup_date == "":
                error = "Invalid pickup date."
            if pickup_time == "":
                error = "Invalid pickup time."
            if timezone_offset == "":
                error = "Invalid timezone offset."

            # Convert the pickup_date and pickup_time to a UTC
            # timestamp for the RideRequest model.
            timestamp_string = str(pickup_date) + " " + str(pickup_time)
            timestamp_string_epoch = datetime.strptime(timestamp_string, "%Y-%m-%d %H:%M").timestamp()
            # Note: the "pickup_timestamp" is adjusted from the user's
            # timezone to a UTC/GMT timestamp epoch.
            print("pickup_timestamp (raw datetime string): " + timestamp_string)
            print("pickup_timestamp (raw epoch):           " + str(timestamp_string_epoch))
            print(timestamp_string_epoch)
            print(timezone_offset)
            pickup_timestamp = int(timestamp_string_epoch) + int(timezone_offset)  # <!-- this is what we need.
            django_pickup_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pickup_timestamp))

            """
            DEBUG CODE @TODO DELETE THIS
            """
            print("pickup_timestamp (adjusted epoch):      " + str(pickup_timestamp))
            """
            END DEBUG CODE
            """
            print("start_address: " + str(start_address))
            print("start_place_id: " + str(start_place_id))
            print("end_address: " + str(end_address))
            print("end_place_id: " + str(end_place_id))
            print("app_user: " + str(app_user))
            print("pickup_timestamp: " + str(pickup_timestamp))

            # Save and create the new RideRequest.
            if ride_request is None:
                # Create the new ride_request.
                ride_request = RideRequest.objects.create(
                    start_address=start_address,
                    start_place_id=start_place_id,
                    end_address=end_address,
                    end_place_id=end_place_id,
                    app_user=app_user,
                    status="REQ_1",
                    pickup_timestamp=str(django_pickup_timestamp),
                    in_setup=True,
                )
            else:
                # Save ("update") the existing ride request.
                ride_request.start_place_id = start_place_id
                ride_request.end_address = end_address
                ride_request.end_place_id = end_place_id
                ride_request.app_user = app_user
                # REQ_1 is the status for an initiated ride request
                # that has not yet been "confirmed" by a passenger.
                ride_request.status = "REQ_1"
                ride_request.pickup_timestamp = str(django_pickup_timestamp)
                ride_request.in_setup = True
                ride_request.save()

            # @TODO persist model

            # If POST and no errors, redirect to main_screen (map).
            if error == "":
                return redirect("/main_screen")

    sidebar_info = RideRequest.rider_sidebar_info(app_user)
    print("FOO")
    print(ride_request)

    context = {
        # Form info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        "sidebar_info": sidebar_info,
        # Page info.
        "ride_request": ride_request,
        "start_address": start_address,
        "end_address": end_address,
        "pickup_timestamp": pickup_timestamp,
    }
    return render(request, "rideshare/pages/set_location.html", context)


def account(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    if sidebar_info is None:
        sidebar_info = RideRequest.rider_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # Page info.
        "phone_number": app_user.phone_number,
    }
    return render(request, "rideshare/pages/account.html", context)


def profile(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    error = ""
    all_pronouns = Pronoun.objects.all()
    all_accommodations = Accommodation.objects.all()

    username = app_user.username
    pronoun = app_user.pronoun
    accommodations = list(app_user.accommodations.all())

    if request.method == "POST":

        if not request.POST:
            error = "Invalid request."
        else:
            username = request.POST.get("username")
            if username is None or username == "":
                error += "Username required. "

            pronoun_id = request.POST.get("pronoun_id")
            if pronoun_id is None or pronoun_id == "":
                error += "Pronoun required. "
            else:
                pronoun = Pronoun.objects.get(id=pronoun_id)

            sel_accommodations = []
            for accommodation in all_accommodations:
                sel_accommodation = request.POST.get(
                    "accommodation_%s" % str(accommodation.id))
                if sel_accommodation is not None:
                    sel_accommodations.append(accommodation)

        if error == "":
            app_user = AppUser.objects.get(django_account=request.user)
            app_user.username = username
            app_user.pronoun = pronoun
            app_user.accommodations.set(sel_accommodations)
            app_user.save()
            return redirect(request.path)

    context = {
        # Post info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # User info.
        "username": username,
        "pronoun": pronoun,
        "accommodations": accommodations,
        # Form info.
        "all_pronouns": all_pronouns,
        "all_accommodations": all_accommodations,
    }
    return render(request, "rideshare/pages/profile.html", context)


def past_rides(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    rides = RideRequest.passenger_past_rides(app_user)
    sidebar_info = RideRequest.rider_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        "sidebar_info": sidebar_info,
        # Page info.
        "rides": rides,
    }
    return render(request, "rideshare/pages/past_rides.html", context)


def upcoming_rides(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    rides = RideRequest.passenger_upcoming_rides(app_user)
    sidebar_info = RideRequest.rider_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        "sidebar_info": sidebar_info,
        # Page info.
        "rides": rides,
    }
    return render(request, "rideshare/pages/upcoming_rides.html", context)


def donation_station(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.rider_sidebar_info(app_user)
    donation_subscriptions = DonationSubscription.objects.filter(
        app_user=app_user,
        success=True,
        deleted=False,
    )

    plans = {
        "Recurring $5 Donation": "plan_GtHMSytV6dBI4w",
        "Recurring $10 Donation": "plan_GtHNLR9qjsDA07",
        "Recurring $20 Donation": "plan_GtHNDPdGf0CHXt",
        "Recurring $50 Donation": "plan_GtHNIuvgQlTHAS",
        "Recurring $75 Donation": "plan_GtHOA2kzudRbVC",
        "Recurring $100 Donation": "plan_GtHOshLsz1TUVA",
        "Recurring $500 Donation": "plan_GtHOHuR5L0c2DO",
        "Recurring $1,000 Donation": "plan_GtHP6n00NgIpaf",
    }

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        "sidebar_info": sidebar_info,
        # Page info.
        "donation_subscriptions": donation_subscriptions,
        "plans": plans,
    }
    return render(request, "rideshare/pages/donation_station.html", context)


def _settings(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    if sidebar_info is None:
        sidebar_info = RideRequest.rider_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # Page info.
    }
    return render(request, "rideshare/pages/settings.html", context)


def about(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    if sidebar_info is None:
        sidebar_info = RideRequest.rider_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # Page info.
    }
    return render(request, "rideshare/pages/about.html", context)


def help(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    if sidebar_info is None:
        sidebar_info = RideRequest.rider_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # Page info.
    }
    return render(request, "rideshare/pages/help.html", context)


def payment_methods(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/payment_methods.html", context)


def email_address(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    error = ""

    email_address = app_user.email_address
    email_verified = app_user.email_verified

    if request.method == "POST":

        if not request.POST:
            error = "Invalid request."
        else:
            email_address = request.POST.get("email_address")
            if email_address is None or email_address == "":
                error += "Email address required. "

        if error == "":
            app_user = AppUser.objects.get(django_account=request.user)
            if email_address != app_user.email_address:
                app_user.email_address = email_address
                app_user.email_verification_code = rs_utils.random_string(64)
                app_user.email_verified = False
                # @TODO send verification email.
                app_user.save()
                return redirect(request.path)

    if request.method == "GET":
        if request.GET:
            email_verification_code = request.GET.get("verification_code")
            app_user = AppUser.objects.get(django_account=request.user)
            if email_verification_code == app_user.email_verification_code:
                app_user.email_verified = True
                app_user.save()
                email_verified = True

    context = {
        # Post info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # Page info.
        "email_address": email_address,
        "email_verified": email_verified,
    }
    return render(request, "rideshare/pages/email_address.html", context)


def phone_number(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    error = ""

    phone_number = app_user.phone_number
    phone_verified = app_user.phone_verified

    if request.method == "POST":

        if not request.POST:
            error = "Invalid request."
        else:
            phone_number = request.POST.get("phone_number")

            if phone_number is not None and phone_number != "":
                app_user = AppUser.objects.get(django_account=request.user)
                app_user.phone_verified = False
                app_user.phone_number = phone_number
                app_user.phone_verification_code = rs_utils.random_phone_code()
                # print("verification code assigned")
                # @TODO Twillio send this code to the phone number.
                # body = "example"
                # to = "+15404540846"

                # send_phone_verification_text(body, to)

                app_user.save()
                info = "Please enter the code we sent you to verify your new number."
                return redirect(request.path)
            else:
                error += "Phone number required."

    context = {
        # Post info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # Page info.
        "phone_number": phone_number,
        "phone_verified": phone_verified,
    }
    return render(request, "rideshare/pages/phone_number.html", context)


"""-----------------------------------------------------------------------------
Settings pages.
-----------------------------------------------------------------------------"""


def services(request, user_type="rider", sidebar_info=None):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    error = ""
    all_accommodations = Accommodation.objects.all()

    accommodations = list(app_user.accommodations.all())

    if request.method == "POST":

        if not request.POST:
            error = "Invalid request."
        else:
            sel_accommodations = []
            for accommodation in all_accommodations:
                sel_accommodation = request.POST.get(
                    "accommodation_%s" % str(accommodation.id))
                if sel_accommodation is not None:
                    sel_accommodations.append(accommodation)

        if error == "":
            app_user = AppUser.objects.get(django_account=request.user)
            app_user.accommodations.set(sel_accommodations)
            app_user.save()
            return redirect(request.path)

    context = {
        # Post info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        "user_type": user_type,
        "sidebar_info": sidebar_info,
        # Paga info.
        "accommodations": accommodations,
        # Form info.
        "all_accommodations": all_accommodations,
    }
    return render(request, "rideshare/pages/services.html", context)


def location(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/location.html", context)


def notifications(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/notifications.html", context)


def emergency(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/emergency.html", context)


def trusted_contacts(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/trusted_contacts.html", context)


def delete_account(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/delete_account.html", context)


"""-----------------------------------------------------------------------------
Help pages.
-----------------------------------------------------------------------------"""


def report_a_recent_ride(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/report_a_recent_ride.html", context)


def report_a_lost_item(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/report_a_lost_item.html", context)


def how_ride_payment_works(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/how_ride_payment_works.html", context)


def free_rides(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/free_rides.html", context)


def saftey(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/saftey.html", context)


def policies(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/policies.html", context)


def legal(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/legal.html", context)


"""-----------------------------------------------------------------------------
Driver pages.
-----------------------------------------------------------------------------"""


def driver(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
        "sidebar_info": sidebar_info,
    }
    return render(request, "rideshare/pages/driver.html", context)


def driver_past_rides(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    rides = RideRequest.driver_past_rides(app_user)
    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
        "rides": rides,
        "sidebar_info": sidebar_info,
    }
    return render(request, "rideshare/pages/driver_past_rides.html", context)


def driver_upcoming_rides(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    rides = RideRequest.driver_upcoming_rides(app_user)
    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
        "rides": rides,
        "sidebar_info": sidebar_info,
    }
    return render(request, "rideshare/pages/driver_upcoming_rides.html", context)


def driver_available_rides(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    rides = RideRequest.driver_availible_rides(app_user)
    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
        "rides": rides,
        "sidebar_info": sidebar_info,
    }
    return render(request, "rideshare/pages/driver_available_rides.html", context)


def driver_notifications(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
        "sidebar_info": sidebar_info,
    }
    return render(request, "rideshare/pages/driver_notifications.html", context)


def driver_account(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    return account(request, user_type="driver",
                   sidebar_info=sidebar_info)


def driver_settings(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    return _settings(request, user_type="driver",
                     sidebar_info = sidebar_info)


def driver_about(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    return about(request, user_type="driver",
                 sidebar_info=sidebar_info)


def driver_help(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    return help(request, user_type="driver",
                sidebar_info=sidebar_info)


"""
Driver /account/
"""

def driver_payment_methods(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    sidebar_info = RideRequest.driver_sidebar_info(app_user)

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
        "sidebar_info": sidebar_info,
    }
    return render(request, "rideshare/pages/driver_payment_methods.html", context)


"""-----------------------------------------------------------------------------
DRIVER ACTIVE RIDE
-----------------------------------------------------------------------------"""


def ride_details(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    id = request.GET.get("id")
    ride_request = RideRequest.objects.get(id=id)
    if ride_request is None:
        raise Exception("Ride not found.")
    if ride_request.app_user != app_user:
        if ride_request.app_user_driver is not None:
            if ride_request.app_user_driver != app_user:
                raise Exception("You don't have permission to view this ride.")
    ride_donation = RideDonation.objects.filter(
        ride_request=ride_request,
        success=True,
    ).first()

    historical = False
    print(ride_request.pickup_timestamp)
    print(type(ride_request.pickup_timestamp))
    from datetime import timezone
    print(datetime.now(timezone.utc))
    print(type(datetime.now(timezone.utc)))
    if ride_request.pickup_timestamp < datetime.now(timezone.utc):
        historical = True
    passenger = False
    if ride_request.app_user == app_user:
        passenger = True
    driver = False
    if ride_request.app_user_driver == app_user:
        driver = True

    context = {
        # Sidebar info.
        "app_user": app_user,
        # Page info.
        "id": id,
        "ride_request": ride_request,
        "ride_donation": ride_donation,
        "historical": historical,
        "passenger": passenger,
        "driver": driver,
    }
    return render(request, "rideshare/pages/ride_details.html", context)


def driver_active_ride(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
    }
    return render(request, "rideshare/pages/driver_active_ride.html", context)


def active_ride(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "driver",
        # Page info.
    }
    return render(request, "rideshare/pages/active_ride.html", context)

"""
STRIPE
"""
def payment_success(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    session_id = request.GET.get("session_id")
    if session_id is None or session_id == "":
        return redirect("/error")

    try:
        donation_subscription = DonationSubscription.find_by_checkout_session_id(
            session_id)
        if donation_subscription is not None:
            import stripe_util
            subscription_id = stripe_util.get_subscription_id_by_session_id(session_id)
            donation_subscription.subscription_id = subscription_id
            donation_subscription.success = True
            donation_subscription.save()

        context = {
            # Sidebar info.
            "app_user": app_user,
            "user_type": "rider",
            # Page info.
            "donation_subscription": donation_subscription,
        }

        return render(request, "rideshare/pages/payment_success.html", context)
    except Exception as ex:
        ride_donation = RideDonation.objects.get(
            checkout_session_id=session_id,
        )
        if ride_donation is not None:
            ride_donation.success = True
            ride_donation.save()

        ride_request_id = ride_donation.ride_request.id

        return redirect("ride_details/?id=%s" % ride_request_id, status=302)


def payment_canceled(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    session_id = request.GET.get("session_id")
    if session_id is None or session_id == "":
        return redirect("/error")

    donation_subscription = DonationSubscription.find_by_checkout_session_id(
        session_id)
    if donation_subscription is not None:
        donation_subscription.success = False
        donation_subscription.save()

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }

    return render(request, "rideshare/pages/payment_canceled.html", context)
