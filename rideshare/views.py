from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import redirect

from rideshare.models import AppUser, Pronoun


def index(request):
    template = loader.get_template("rideshare/pages/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def phone_verification(request):
    if request.user.is_authenticated == False:
        return redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(django_account=request.user)
    if app_user.phone_number is not None:
        return redirect("/code_verification")
    context = {
        "user_id": request.user.id,
        "app_user": app_user,
        "phone_number": app_user.phone_number,
        "phone_verified": app_user.phone_verified,
    }
    return render(request, "rideshare/pages/phone_verification.html", context)

def code_verification(request):
    if request.user.is_authenticated == False:
        return redirect("/accounts/login")
    app_user, created = AppUser.objects.get_or_create(django_account=request.user)
    if app_user.phone_verified == True:
        return redirect("/main_screen")
    context = {}
    return render(request, "rideshare/pages/code_verification.html", context)

def main_screen(request):
    if request.user.is_authenticated == False:
        return redirect("/accounts/login")
    context = {}
    return render(request, "rideshare/pages/main_screen.html", context)

def set_location(request):
    if request.user.is_authenticated == False:
        return redirect("/accounts/login")
    context = {}
    return render(request, "rideshare/pages/set_location.html", context)

def account(request):
    if request.user.is_authenticated == False:
        return redirect("/account/login")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user
    )
    if app_user.phone_verified == False:
        return redirect("/phone_verification")
    if app_user.phone_number is None:
        return redirect("/phone_verification")
    context = {
        "phone_number": app_user.phone_number,
    }
    return  render(request, "rideshare/pages/account.html", context)

def profile(request):
    if request.user.is_authenticated == False:
        return redirect("/accounts/login")
    app_user, created = AppUser.objects.get_or_create(
        django_account=request.user
    )
    pronouns = Pronoun.objects.all()
    context = {
        "username": app_user.username,
        "pronoun": app_user.pronoun,
        "accommodations": None,
        "pronouns": pronouns,
    }
    return render(request, "rideshare/pages/profile.html", context)
