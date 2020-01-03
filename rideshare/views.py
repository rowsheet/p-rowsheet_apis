import os
from django.http import HttpResponse
from django.template import loader

menu = {
        "index": "",
        "main_screen": "main_screen",
        "verification_phone": "verification_phone",
        "verification_code": "verification_code",
        "set_location": "set_location",
        "set_location_later": "set_location_later",
        "create_account": "create_account",
        "account_created": "account_created",
        "account": "account",
}

def index(request):
    template = loader.get_template("rideshare/pages/initial_screen.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def main_screen(request):
    template = loader.get_template("rideshare/pages/main_screen.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def verification_phone(request):
    template = loader.get_template("rideshare/pages/verification_phone.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def verification_code(request):
    template = loader.get_template("rideshare/pages/verification_code.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def set_location(request):
    template = loader.get_template("rideshare/pages/set_location.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def set_location_later(request):
    template = loader.get_template("rideshare/pages/set_location_later.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def create_account(request):
    template = loader.get_template("rideshare/pages/create_account.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def account_created(request):
    template = loader.get_template("rideshare/pages/account_created.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))

def account(request):
    template = loader.get_template("rideshare/pages/account.html")
    context = {"menu": menu}
    return HttpResponse(template.render(context, request))
