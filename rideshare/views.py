from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

from rideshare.models import AppUser, Pronoun, Accommodation

import rowsheet.utils as rs_utils

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


def index(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user)
    print("INDEX")
    context = {
        # Sidebar info.
        "app_user": app_user,
        # Page info.
    }
    return render(request, "rideshare/pages/index.html", context)


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


def set_location(request):
    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
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
