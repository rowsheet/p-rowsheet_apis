from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import redirect
# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from rideshare.models import AppUser
from rideshare.models import Pronoun
from rideshare.models import Accommodation
from rideshare.models import RideRequest
from rideshare.models import OldRideRequest
from rideshare.models import OldDriverSignup

import rowsheet.utils as rs_utils
import requests
import json


ROWSHEET_EMAILER_KEY = "BfpKNjGwMOsC67DDfuzUQqQPnMLAP2l"
RECAPTCHA_SECRET = "6LeoZbYUAAAAAJAN7NGGbFuT8qNKGPdKyqG6IgRR"
RECAPTCHA_MIN_SCORE = "0.7"

from twilio.rest import Client

def send_text_message(body):
    account_sid = "AC24fc9ac27dee145f04d855b99b666ab8"
    auth_token  = "08da7fc65a1b8163f17aa324ddef479d"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        # to="+15404540846",
        # to="+17203643760",
        to="+14155745023",
        from_="+14159939395",
        body=body)

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
            send_text_message("Ride request from: " + data.get("name"))
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
            return HttpResponse("GOT REQUEST RIDE", status=200)
        if command == "driver_signup":
            OldDriverSignup.objects.create(
                comments=data.get("comments"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                contact_email=data.get("contact_email"),
                contact_phone=data.get("contact_phone"),
                pronoun=data.get("pronoun"),
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

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
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
    start_address = "sa"
    start_place_id = "spi"
    end_address = "ea"
    end_place_id = "epi"
    ride_utc = "ru" # @ToDo Make timestamp field in model.
    try:
        ride_request = RideRequest.objects.get(
            app_user=app_user,
        )
        if ride_request is not None:
            print("GOT RIDE REQUEST")
        else:
            print("NO RIDE REQUEST")
    except Exception as ex:
        ride_request = None

    error = ""

    if request.method == "POST":
        print("GOT POST")
        if not request.POST:
            error = "Invalid request."
        return JsonResponse({
            "data": "TEST DATA",
        }, status=200)

    context = {
        # Form info.
        "error": error,
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
        "ride_request": ride_request,
        "start_address": start_address,
        "start_place_id": start_place_id,
        "end_address": end_address,
        "end_place_id": end_place_id,
        "ride_utc": ride_utc,
    }
    return render(request, "rideshare/pages/set_location.html", context)


def account(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
        "phone_number": app_user.phone_number,
    }
    return render(request, "rideshare/pages/account.html", context)


def profile(request):
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
        "user_type": "rider",
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

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/past_rides.html", context)


def donation_station(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/donation_station.html", context)


def settings(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/settings.html", context)


def driver(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/driver.html", context)


def about(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
    }
    return render(request, "rideshare/pages/about.html", context)


def help(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
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


def email_address(request):
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
        "user_type": "rider",
        # Page info.
        "email_address": email_address,
        "email_verified": email_verified,
    }
    return render(request, "rideshare/pages/email_address.html", context)

def phone_number(request):
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
                # @TODO Twillio send this code to the phone number.
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
        "user_type": "rider",
        # Page info.
        "phone_number": phone_number,
        "phone_verified": phone_verified,
    }
    return render(request, "rideshare/pages/phone_number.html", context)


"""-----------------------------------------------------------------------------
Settings pages.
-----------------------------------------------------------------------------"""


def services(request):
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
        "user_type": "rider",
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
