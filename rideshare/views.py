from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import redirect

from rideshare.models import AppUser, Pronoun, Accommodation


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
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user)
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
    context = {
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
    context = {
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
        "app_user": app_user,
        "user_type": "rider",
        # Sidebar info.
        "phone_number": app_user.phone_number,
        # Page info.
    }
    return render(request, "rideshare/pages/account.html", context)


def profile(request):

    app_user, user_redirect = load_app_user(request)
    if user_redirect is not None:
        return user_redirect

    pronouns = Pronoun.objects.all()
    accommodations = Accommodation.objects.all()
    context = {
        # Sidebar info.
        "app_user": app_user,
        "user_type": "rider",
        # Page info.
        "username": app_user.username,
        "pronoun": app_user.pronoun,
        "accommodation": app_user.accommodation,
        "pronouns": pronouns,
        "accommodations": accommodations,
    }
    return render(request, "rideshare/pages/profile.html", context)
