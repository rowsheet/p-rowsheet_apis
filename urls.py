import uuid
import base64
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings

from rowsheet.api import handle

admin.autodiscover()

auth_nonce = settings.AUTH_NONCE

def auth(request):
    if request.user.is_authenticated:
        print("Authenticated.")
        return JsonResponse({ "session_id": request.session.session_key }, status=200)
    else:
        nonce = request.GET.get("nonce")
        if nonce is None:
            print("Unauthorized: no nonce.")
            return JsonResponse({ "error": "Unauthorized." }, status=401)
        session_key = auth_nonce.get(nonce)
        response = { "session_id": session_key }
        if session_key is None:
            print("Invalid nonce.")
            return JsonResponse({ "error": "Invalid nonce." }, status=400)
        print("Valid nonce.")
        return JsonResponse({ "session_id": session_key }, status=200)

def set_nonce(request):
    if request.user.is_authenticated:
        nonce = str(uuid.uuid4())
        auth_nonce.set(nonce, request.session.session_key)
        return HttpResponseRedirect(settings.WEBAPP_URL + "/auth_callback?auth_nonce=" + nonce, 302)
    return JsonResponse({ "error": "Unauthorized." }, status=401)

def logout_callback(request):
    return HttpResponseRedirect(settings.WEBAPP_URL, 302)

def parse_auth_bearer(request):
    try:
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        print("auth_header: " + auth_header)
        auth_type = auth_header.split(' ')[0]
        credentials = auth_header.split(' ')[1]
        if auth_type == "Bearer":
            return credentials
        decoded_credentials = base64.b64decode(credentials).decode("utf-8")
        print("decoded_credentials: " + str(decoded_credentials))
        bearer = decoded_credentials.split(':')[0][1:-1]
        return bearer
    except Exception as ex:
        print(str(ex))
        return ""

@csrf_exempt
def session(request):
    bearer_token = parse_auth_bearer(request)
    print("TOKEN: " + str(bearer_token))
    try:
        session = Session.objects.get(session_key=bearer_token)
        return JsonResponse({"data": "OK"}, status=200)
    except Exception as ex:
        print(str(ex))
        return JsonResponse({"error": "Unauthorized" }, status=401)

def catch_all(request):
        return HttpResponseRedirect("/docs/v1")

"""
def info(request):
    import pprint as pp
    data = "%s<br><pre>%s</pre>" % (
        request.build_absolute_uri(),
        # pp.pformat(request.META),
        # "foo",
        pp.pprint(auth_nonce)
    )
    return HttpResponse(data, status=200)
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^docs/", include("rowsheet.urls")),
    path("<version>/<service>/<module>/<command>", handle),
    # path("info", info),
    path("auth", auth),
    path("set_nonce", set_nonce),
    path("logout_callback", logout_callback),
    path("session", session),
    path("", catch_all),
]
