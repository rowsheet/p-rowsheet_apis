from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.shortcuts import redirect

from rideshare.models import AppUser


def index(request):
    template = loader.get_template("rideshare/pages/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def phone_verification(request):
    if request.user.is_authenticated == False:
        return redirect("/accounts/login/")
    app_user, created = AppUser.objects.get_or_create(django_account=request.user)
    import pprint as pp
    pp.pprint(app_user)
    print(app_user.username)
    if app_user.phone_verified == True:
        redirect("/main_screen")
    context = {
        "user_id": request.user.id,
        "app_user": app_user,
        "phone_number": app_user.phone_number,
        "phone_verified": app_user.phone_verified,
    }
    return render(request, "rideshare/pages/phone_verification.html", context)

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
