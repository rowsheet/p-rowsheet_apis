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


def index(request):
    template = loader.get_template("rideshare/pages/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def phone_verification(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user)
    context = {
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
    context = {}
    return render(request, "rideshare/pages/code_verification.html", context)


def main_screen(request):

    app_user, redirect = load_app_user(request)
    if redirect is not None:
        return redirect

    context = {}
    return render(request, "rideshare/pages/main_screen.html", context)


def set_location(request):

    app_user, redirect = load_app_user(request)
    if redirect is not None:
        return redirect

    context = {}
    return render(request, "rideshare/pages/set_location.html", context)


def account(request):

    app_user, redirect = load_app_user(request)
    if redirect is not None:
        return redirect

    context = {
        "phone_number": app_user.phone_number,
    }
    return render(request, "rideshare/pages/account.html", context)


def profile(request):

    app_user, redirect = load_app_user(request)
    if redirect is not None:
        return redirect

    pronouns = Pronoun.objects.all()
    accommodations = Accommodation.objects.all()
    context = {
        "username": app_user.username,
        "pronoun": app_user.pronoun,
        "accommodation": app_user.accommodation,
        "pronouns": pronouns,
        "accommodations": accommodations,
    }
    return render(request, "rideshare/pages/profile.html", context)
